# import shap
import matplotlib.pyplot as plt
import pandas as pd
import globals
import numpy as np
import subprocess
import os
import pm4py
from xgboost import XGBClassifier
from filehelper import gather_all_xes, get_all_ready_logs
from feature_controller import read_feature_matrix, read_feature_vector
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


def extract_regression_method(s):
    prefix = "regression_based_"
    if s.startswith(prefix):
        return s[len(prefix):]
    else:
        # or raise an error if you prefer
        print(f"Invalid regression based classification method {s}")
        sys.exit(-1)


def compute_fitted_regressor(regression_method, discovery_algorithm, measure_name, ready_training, feature_portfolio):
    x_train = read_feature_matrix(ready_training, feature_portfolio)
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
        reg = RandomForestRegressor()
    elif regression_method == "gradient_boosting":
        reg = GradientBoostingRegressor(n_estimators=100)
    elif regression_method == "polynomial_regression":
        reg = make_pipeline(PolynomialFeatures(degree=10), LinearRegression())
    elif regression_method == "svm":
        reg = SVR()
    elif regression_method == "knn":
        reg = KNeighborsRegressor(n_neighbors=5)
    elif regression_method == "mlp":
        reg = MLPRegressor(max_iter=1000)
    elif regression_method == "xgboost":
        reg = XGBRegressor(objective='reg:squarederror')
    else:
        raise ValueError(
            f"Invalid regression method: {regression_method}")

    reg = reg.fit(x_train, y_train)

    return reg


def read_fitted_regressor(regression_method, discovery_algorithm, measure_name, ready_training, feature_portfolio):
    regressor_filepath = f"./cache/regressors/{discovery_algorithm}_regressors/{discovery_algorithm}_{measure_name}_{regression_method}.pkl"
    try:
        ret = load_cache_variable(regressor_filepath)
    except Exception:
        print("Regressor doesn't exist yet. Computing regressor now")

        ret = compute_fitted_regressor(
            regression_method, discovery_algorithm, measure_name, ready_training, feature_portfolio)

        store_cache_variable(ret, regressor_filepath)

    return ret


def regression(log_path, regression_method, discovery_algorithm, measure_name, ready_training, feature_portfolio):

    reg = read_fitted_regressor(
        regression_method, discovery_algorithm, measure_name, ready_training, feature_portfolio)

    predictions = reg.predict(read_feature_vector(log_path, feature_portfolio))

    return predictions[0]


def regression_based_classification(log_path, classification_method, measure_name, ready_training, feature_portfolio, algorithm_portfolio):
    regression_method = extract_regression_method(classification_method)
    value_list = {discovery_algorithm: regression(log_path, regression_method, discovery_algorithm, measure_name,
                                                  ready_training, feature_portfolio) for discovery_algorithm in globals.algorithm_portfolio}

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
    X = read_feature_matrix(all_log_paths, globals.selected_features)
    y = read_regression_target_vector(
        all_log_paths, discovery_algorithm, measure_name)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)
    rf_default = RandomForestRegressor(random_state=42)
    rf_default.fit(X_train, y_train)
    y_pred_default = rf_default.predict(X_test)
    mse_default = mean_squared_error(y_test, y_pred_default)
    print("MSE (Before Optimization):", mse_default)

    # 2. Hyperparameter Optimization Using GridSearchCV
    # Ensuring a consistent random state for reproducibility
    rf = RandomForestRegressor(random_state=42)
    grid_search = GridSearchCV(
        estimator=rf, param_grid=param_grid, cv=5, verbose=2, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    print("Best parameters found: ", grid_search.best_params_)

    # 3. RandomForestRegressor With Optimized Parameters (After Optimization)
    rf_optimized = RandomForestRegressor(
        **grid_search.best_params_, random_state=42)
    rf_optimized.fit(X_train, y_train)
    y_pred_optimized = rf_optimized.predict(X_test)
    mse_optimized = mean_squared_error(y_test, y_pred_optimized)
    print("MSE (After Optimization):", mse_optimized)

    # 4. Compare the MSEs
    print("MSE Improvement:", mse_default - mse_optimized)
    return grid_search.best_params_


def get_xgboost_optimal_parameters(all_log_paths, discovery_algorithm, measure_name):
    X = read_feature_matrix(all_log_paths, globals.selected_features)
    y = read_regression_target_vector(
        all_log_paths, discovery_algorithm, measure_name)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)

    # 1. Baseline Model
    xgb_reg = XGBRegressor(objective='reg:squarederror', random_state=42)
    xgb_reg.fit(X_train, y_train)
    y_pred_default = xgb_reg.predict(X_test)
    mse_default = mean_squared_error(y_test, y_pred_default)
    print("MSE (Before Optimization):", mse_default)

    # 2. Hyperparameter Optimization
    # Define a parameter grid to search through
    param_grid = {
        'n_estimators': [100, 500, 1000, 2000],
        'learning_rate': [0.05, 0.1, 0.2],
        'max_depth': [3, 5, 7],
        'colsample_bytree': [0.7, 1],
        # Add more parameters here
    }

    grid_search = GridSearchCV(
        estimator=XGBRegressor(objective='reg:squarederror', random_state=42),
        param_grid=param_grid,
        cv=5,
        verbose=2,
        n_jobs=-1
    )

    grid_search.fit(X_train, y_train)
    print("Best parameters found: ", grid_search.best_params_)

    # 3. XGBoost Regressor With Optimized Parameters
    xgb_optimized = XGBRegressor(
        **grid_search.best_params_,
        objective='reg:squarederror',
        random_state=42
    )
    xgb_optimized.fit(X_train, y_train)
    y_pred_optimized = xgb_optimized.predict(X_test)
    mse_optimized = mean_squared_error(y_test, y_pred_optimized)
    print("MSE (After Optimization):", mse_optimized)
    print("MSE Improvement:", mse_default - mse_optimized)

    return grid_search.best_params_


if __name__ == "__main__":
    feature_dict = get_total_feature_functions_dict()
    feature_list = list(feature_dict.keys())
    globals.selected_features = feature_list

    all_log_paths = get_all_ready_logs(gather_all_xes(
        "../logs"), globals.selected_features, globals.algorithm_portfolio, globals.measures_list)

    get_xgboost_optimal_parameters(all_log_paths, "split", "pm4py_simplicity")
    # get_random_forest_optimal_parameters(X, y)
