# import shap
import matplotlib.pyplot as plt
import pandas as pd
import globals
import numpy as np
import subprocess
import os
import pm4py
from xgboost import XGBClassifier
from utils import read_logs, read_models,  get_all_ready_logs
from filehelper import gather_all_xes, get_all_ready_logs
from feature_controller import read_feature_matrix, read_feature_vector
from measures import read_measure_entry, read_regression_target_vector
from feature_selection import classification_read_optimal_features
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


if __name__ == "__main__":
    globals.algorithm_portfolio = ["alpha", "heuristic",
                                   "inductive", "ILP", "split"]

    feature_dict = get_total_feature_functions_dict()

    feature_list = list(feature_dict.keys())

    globals.selected_features = feature_list
    globals.measures_list = ["token_fitness", "token_precision",
                             "no_total_elements", "generalization", "pm4py_simplicity"]

    globals.classification_methods = [
        x for x in globals.classification_methods if x not in ["knn", "svm"]]

    feature_list = []
    for measure_name in globals.measures_list:
        feature_list += read_optimal_features(
            [], "xgboost", measure_name, feature_list, globals.algorithm_portfolio)

    globals.selected_features = feature_list
    all_logs = gather_all_xes("../logs/testing")
    ready_logs = get_all_ready_logs_multiple(all_logs)[:50]

    algorithm_portfolio = globals.algorithm_portfolio

    classification_method = "xgboost"
    measure_name1 = "token_fitness"
    measure_name2 = "token_precision"

    measure_weight_dict = {measure: 0 for measure in globals.measures_list}
    measure_weight_dict[measure_name1] = 1
    measure_weight_dict[measure_name2] = 1

    for log_path in ready_logs:
        for regression_method in globals.regression_methods:
            for discovery_algorithm in globals.algorithm_portfolio:
                for measure_name in globals.measures_list:
                    val1 = regression_based_classification(
                        log_path, f"regression_based_{regression_method}", measure_name, ready_logs, feature_list, algorithm_portfolio)
