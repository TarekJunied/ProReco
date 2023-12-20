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
from filehelper import gather_all_xes, get_all_ready_logs, get_all_ready_logs_multiple
from feature_controller import read_feature_matrix, read_feature_vector
from measures import read_measure_entry, read_regression_target_vector
from init import *
from autofolio_interface import autofolio_classification
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from lime import lime_tabular
from sklearn.tree import plot_tree


def read_multiobjective_graph(log_path, ready_training, measure_weight_dict, regression_method="linear_regression"):
    predicted_alg_values = {}
    relevant_measures = [key for key,
                         value in measure_weight_dict.items() if value > 0]
    predicted_algorithm_vectors = {algorithm: []
                                   for algorithm in globals.algorithm_portfolio}
    actual_algorithm_vectors = {algorithm: []
                                for algorithm in globals.algorithm_portfolio}

    for discovery_algorithm in globals.algorithm_portfolio:
        for measure_name in relevant_measures:
            predicted_value = regression(
                log_path, regression_method, measure_name, discovery_algorithm, ready_training)
            actual_value = read_measure_entry(
                log_path, discovery_algorithm, measure_name)
            predicted_alg_values[discovery_algorithm,
                                 measure_name] = predicted_value
            predicted_algorithm_vectors[discovery_algorithm].append(
                predicted_value)
            actual_algorithm_vectors[discovery_algorithm].append(actual_value)

    n = len(globals.algorithm_portfolio)
    predicted_dominated = set()
    actual_dominated = set()
    for i in range(n):
        for j in range(n):
            algo_i = globals.algorithm_portfolio[i]
            algo_j = globals.algorithm_portfolio[j]
            if algo_i_dominates_algo_j(predicted_algorithm_vectors[algo_i], predicted_algorithm_vectors[algo_j], relevant_measures):
                predicted_dominated.add(algo_j)
            if algo_i_dominates_algo_j(actual_algorithm_vectors[algo_i], actual_algorithm_vectors[algo_j], relevant_measures):
                actual_dominated.add(algo_j)

    print(f"predicted dominated algos {predicted_dominated}")
    print(f"acutal dominated algos {actual_dominated}")

    m = max(len(predicted_dominated), len(actual_dominated))
    u = len(predicted_dominated.intersection(actual_dominated))

    return u/m


def algo_i_dominates_algo_j(algo_i_value_vector, algo_j_value_vector, relevant_measures):
    i_dominates_j = True
    k = 0
    for measure in relevant_measures:
        if globals.measures_kind[measure] == "max":
            if algo_i_value_vector[k] <= algo_j_value_vector[k]:
                i_dominates_j = False
            elif globals.measures_kind[measure] == "min":
                if algo_i_value_vector[k] >= algo_j_value_vector[k]:
                    i_dominates_j = False
                else:
                    print("fuck")
                k += 1
    return i_dominates_j
