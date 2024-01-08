# import shap
import matplotlib.pyplot as plt
import pandas as pd
import math
import globals
import numpy as np
import sys
import subprocess
import os
import pm4py
from xgboost import XGBClassifier
from filehelper import gather_all_xes, get_all_ready_logs
from feature_controller import read_feature_matrix, read_feature_vector, read_single_feature
from utils import load_cache_variable, split_data, get_log_name
from measures import read_measure_entry, read_regression_target_vector
from init import *
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.tree import plot_tree
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from feature_controller import get_total_feature_functions_dict


def read_optimal_features(regression_method, discovery_algorithm, measure_name):
    file_path = f"./cache/optimal_features_lists/regression/{regression_method}/optimal_features_{discovery_algorithm}_{measure_name}.pk"
    try:
        optimal_features_list = load_cache_variable(file_path)
    except Exception:
        optimal_features_list = globals.feature_portfolio
    return optimal_features_list


def extract_regression_method(s):
    prefix = "regression_based_"
    if s.startswith(prefix):
        return s[len(prefix):]
    else:
        # or raise an error if you prefer
        print(f"Invalid regression based classification method {s}")
        sys.exit(-1)


def get_optimized_xgboost_regressor(x_train, y_train):
    # Initial XGBRegressor
    reg = XGBRegressor(objective='reg:squarederror')

    # Hyperparameter Optimization
    param_grid = {
        'n_estimators': [100, 500, 1000, 200],
        'learning_rate': [0.05, 0.1, 0.2, 0.3],
        'max_depth': [3, 5, 7, 9, 11],
        'colsample_bytree': [0.7, 0.8, 1],
        # Add more parameters here
    }

    grid_search = GridSearchCV(
        estimator=reg,
        param_grid=param_grid,
        cv=5,
        verbose=2,
        n_jobs=-1
    )

    grid_search.fit(x_train, y_train)
    print("Best parameters found: ", grid_search.best_params_)

    # Using optimized parameters to fit the regressor
    reg = XGBRegressor(
        **grid_search.best_params_,
        objective='reg:squarederror'
    )
    return reg


def get_optimized_random_forest_regressor(x_train, y_train):
    # Initial RandomForestRegressor
    reg = RandomForestRegressor()

    # Hyperparameter Optimization
    param_grid = {
        'n_estimators': [100, 200, 500, 100],
        'max_depth': [None, 10, 20, 30, 40],
        'min_samples_split': [2, 5, 10, 20],
        'min_samples_leaf': [1, 2, 4, 8],
        'max_features': ['auto', 'sqrt']
        # Add more parameters here
    }

    grid_search = GridSearchCV(
        estimator=reg,
        param_grid=param_grid,
        cv=5,
        verbose=2,
        n_jobs=-1
    )

    grid_search.fit(x_train, y_train)
    print("Best parameters found: ", grid_search.best_params_)

    # Using optimized parameters to fit the regressor
    reg = RandomForestRegressor(
        **grid_search.best_params_
    )
    return reg


def compute_fitted_regressor(regression_method, discovery_algorithm, measure_name, ready_training):

    optimal_features = read_optimal_features(
        regression_method, discovery_algorithm, measure_name)

    x_train = read_feature_matrix(ready_training, optimal_features)

    y_train = read_regression_target_vector(
        ready_training, discovery_algorithm, measure_name)

    if regression_method == "linear_regression":
        reg = LinearRegression()
    elif regression_method == "ridge_regression":
        reg = Ridge()
    elif regression_method == "lasso_regression":
        reg = Lasso()
    elif regression_method == "decision_tree":
        reg = DecisionTreeRegressor()
    elif regression_method == "random_forest":
        # reg = get_optimized_random_forest_regressor(x_train, y_train)
        # reg
        reg = RandomForestRegressor()
    elif regression_method == "gradient_boosting":
        reg = GradientBoostingRegressor(n_estimators=100)
    elif regression_method == "svm":
        reg = SVR()
    elif regression_method == "knn":
        reg = KNeighborsRegressor(n_neighbors=5)
    elif regression_method == "mlp":
        reg = MLPRegressor(max_iter=10000)
    elif regression_method == "xgboost":
        # reg = get_optimized_xgboost_regressor(x_train, y_train)
        # return reg
        reg = XGBRegressor()
    else:
        raise ValueError(
            f"Invalid regression method: {regression_method}")

    reg = reg.fit(x_train, y_train)

    return reg


def read_fitted_regressor(regression_method, discovery_algorithm, measure_name, ready_training):
    cache_dir = f"./cache/regressors/{discovery_algorithm}_regressors"
    regressor_filepath = f"{cache_dir}/{discovery_algorithm}_{measure_name}_{regression_method}.pkl"
    if (regression_method, discovery_algorithm, measure_name) in globals.regressors:
        print(
            f"read regresssor {regression_method} {discovery_algorithm} {measure_name} from main memory")
        return globals.regressors[regression_method, discovery_algorithm, measure_name]

    try:
        ret = load_cache_variable(regressor_filepath)
    except Exception:
        print("Regressor doesn't exist yet. Computing regressor now")

        ret = compute_fitted_regressor(
            regression_method, discovery_algorithm, measure_name, ready_training)

        os.makedirs(cache_dir, exist_ok=True)

        store_cache_variable(ret, regressor_filepath)
        globals.regressors[regression_method,
                           discovery_algorithm, measure_name] = ret

    return ret


def regression(log_path, regression_method, discovery_algorithm, measure_name, ready_training):

    reg = read_fitted_regressor(
        regression_method, discovery_algorithm, measure_name, ready_training)

    optimal_features = read_optimal_features(
        regression_method, discovery_algorithm, measure_name)

    feature_vector = read_feature_vector(log_path, optimal_features)

    predictions = reg.predict(feature_vector)

    return float(max(min(predictions[0], 1), 0))


def regression_based_classification(log_path, classification_method, measure_name, ready_training):
    regression_method = extract_regression_method(classification_method)
    value_list = {discovery_algorithm: regression(log_path, regression_method, discovery_algorithm, measure_name,
                                                  ready_training) for discovery_algorithm in globals.algorithm_portfolio}

    if globals.measures_kind[measure_name] == "max":
        ret = max(value_list, key=value_list.get)
    elif globals.measures_kind[measure_name] == "min":
        ret = min(value_list, key=value_list.get)
    else:
        print("Invalid measure name")
        sys.exit(-1)

    return ret


def get_regression_based_classification_methods():
    return [f"regression_based_{regression_method}" for regression_method in globals.regression_methods]


def get_random_forest_optimal_parameters(all_log_paths, discovery_algorithm, measure_name):
    X = read_feature_matrix(all_log_paths, globals.feature_portfolio)
    y = read_regression_target_vector(
        all_log_paths, discovery_algorithm, measure_name)
    param_grid = {
        'n_estimators': [100, 200],  # Number of trees in the forest
        # Number of features to consider at every split
        'max_features': ['auto', 'sqrt'],
        'max_depth': [10, 20, None],  # Maximum number of levels in tree
        # Minimum number of samples required to split a node
        'min_samples_split': [2, 5],
        # Minimum number of samples required at each leaf node
        'min_samples_leaf': [1, 2],
        # Method of selecting samples for training each tree
        'bootstrap': [True, False]
    }

    # Initialize the regressor
    rf = RandomForestRegressor()

    # Initialize the Grid Search model
    grid_search = GridSearchCV(
        estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)

    # Fit the grid search to the data
    grid_search.fit(X, y)

    # Print the best parameters found
    print("Best parameters found: ", grid_search.best_params_)

    # Return the best parameters
    return grid_search.best_params_


def init_regressors(ready_training, regression_method):
    for discovery_algorithm in globals.algorithm_portfolio:
        for measure in globals.measure_portfolio:
            read_fitted_regressor(
                regression_method, discovery_algorithm, measure, ready_training)


if __name__ == "__main__":
    feature_dict = get_total_feature_functions_dict()
    feature_list = list(feature_dict.keys())
    globals.feature_portfolio = feature_list

    all_log_paths = get_all_ready_logs(gather_all_xes(
        "../logs"), globals.feature_portfolio, globals.algorithm_portfolio, globals.measure_portfolio)

    ready_training, _ = split_data(all_log_paths)

    regression_method = sys.argv[1]
    discovery_algorithm = sys.argv[2]
    measure = sys.argv[3]

    read_fitted_regressor(regression_method, discovery_algorithm,
                          measure, ready_training)
    # get_random_forest_optimal_parameters(X, y)
