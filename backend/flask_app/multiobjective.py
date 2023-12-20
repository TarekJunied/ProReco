
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
from feature_selection import read_optimal_features
from measures import read_measure_entry, read_regression_target_vector, read_target_entry
from init import *
from classifiers import read_fitted_classifier
from regressors import regression_based_classification, regression
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


def is_regression_based_classification_method_string(classification_method):
    s = classification_method
    return s.startswith("regression_based_") and s.split("regression_based_", 1)[1] in globals.regression_methods


def predicted_classification_ranking_list(log_path, classification_method, measure_name, ready_training, feature_portfolio, algorithm_portfolio):
    clf = read_fitted_classifier(
        classification_method, measure_name, ready_training, feature_portfolio)

    # Read the feature vector
    feature_vector = read_feature_vector(log_path, feature_portfolio)

    # Get predictions with associated probabilities
    predictions = clf.predict_proba(feature_vector)

    # Initialize a dictionary for all classes in algorithm_portfolio with a default probability
    class_probabilities = {
        class_label: 0 for class_label in algorithm_portfolio}

    # Update the dictionary with actual probabilities from the classifier
    for class_label, prob in zip(clf.classes_, predictions[0]):
        class_probabilities[class_label] = prob

    # Sort the dictionary based on probabilities to get the final sorted list
    sorted_predictions = sorted(
        class_probabilities.items(), key=lambda x: x[1], reverse=True)

    # Return only the class labels, sorted from best to worst
    return [label for label, _ in sorted_predictions]


def actual_classification_ranking_list(log_path, measure_name, algorithm_portfolio):
    value_dict = {discovery_algorithm: read_measure_entry(
        log_path, discovery_algorithm, measure_name) for discovery_algorithm in algorithm_portfolio}

    sorted_dict = sorted(value_dict, key=lambda k: value_dict[k], reverse=True)

    return sorted_dict


def predicted_one_dimensional_score_of_discovery_algorithm(log_path_to_predict, discovery_algorithm, classification_method, measure, ready_training, feature_portfolio, algorithm_portfolio):
    """ returns a score of the discovery algorithm on a certain measure
    with 1 being the lowest score and n being the highest score
    for n discovery algorithms

    Args:
        log_path_to_predcit: _description_
        classification_method: _description_
        ready_training: _description_
        feature_portfolio: _description_
        algorithm_portfolio: _description_
    """
    ranking = predicted_classification_ranking_list(
        log_path_to_predict, classification_method, measure, ready_training, feature_portfolio, algorithm_portfolio)

    inverse_score = ranking.index(discovery_algorithm)

    n = len(algorithm_portfolio)

    return n - inverse_score


def actual_one_dimensional_score_of_discovery_algorithm(log_path_to_predict, discovery_algorithm,  algorithm_portfolio):
    """ returns a score of the discovery algorithm on a certain measure
    with 1 being the lowest score and n being the highest score
    for n discovery algorithms

    Args:
        log_path_to_predcit: _description_
        classification_method: _description_
        ready_training: _description_
        feature_portfolio: _description_
        algorithm_portfolio: _description_
    """
    ranking = actual_classification_ranking_list(
        log_path_to_predict, measure_name, algorithm_portfolio)

    inverse_score = ranking.index(discovery_algorithm)

    n = len(algorithm_portfolio)

    return n - inverse_score


def predicted_classification_based_combined_score_of_discovery_algorithm(log_path_to_predict, discovery_algorithm, classification_method, measure_weight_dict, ready_training, feature_portfolio, algorithm_portfolio):
    total_score = 0
    for measure in measure_weight_dict:
        measure_weight = measure_weight_dict[measure]
        measure_score = predicted_one_dimensional_score_of_discovery_algorithm(
            log_path_to_predict, discovery_algorithm, classification_method, measure, ready_training, feature_portfolio, algorithm_portfolio)
        total_score += measure_weight * measure_score

    return total_score


def actual_classification_based_combined_score_of_discovery_algorithm(log_path_to_predict, discovery_algorithm, measure_weight_dict, algorithm_portfolio):
    total_score = 0
    for measure in measure_weight_dict:
        measure_weight = measure_weight_dict[measure]
        measure_score = actual_one_dimensional_score_of_discovery_algorithm(
            log_path_to_predict, discovery_algorithm,  algorithm_portfolio)
        total_score += measure_weight * measure_score

    return total_score


def predicted_regression_based_combined_score_of_discovery_algorithm(log_path_to_predict, discovery_algorithm, regression_method, measure_weight_dict, ready_training, feature_portfolio, algorithm_portfolio):
    total_score = 0
    for measure in measure_weight_dict:
        measure_weight = measure_weight_dict[measure]
        measure_score = regression(log_path_to_predict, regression_method,
                                   discovery_algorithm, measure, ready_training, feature_portfolio)
        total_score += measure_weight * measure_score

    return total_score


def actual_regression_based_combined_score_of_discovery_algorithm(log_path_to_predict, discovery_algorithm, measure_weight_dict):
    total_score = 0
    for measure in measure_weight_dict:
        measure_weight = measure_weight_dict[measure]
        measure_score = read_measure_entry(
            log_path_to_predict, discovery_algorithm, measure)
        total_score += measure_weight * measure_score

    return total_score


def predicted_classification_based_scalarization(log_path_to_predict, classification_method, measure_weight_dict, ready_training, feature_portfolio, algorithm_portfolio):
    ret = {discovery_algorithm: predicted_classification_based_combined_score_of_discovery_algorithm(log_path_to_predict, discovery_algorithm, classification_method,
                                                                                                     measure_weight_dict, ready_training, feature_portfolio, algorithm_portfolio) for discovery_algorithm in algorithm_portfolio}
    return ret


def actual_classification_based_scalarization(log_path_to_predict, measure_weight_dict, algorithm_portfolio):
    ret = {discovery_algorithm: actual_classification_based_combined_score_of_discovery_algorithm(
        log_path_to_predict, discovery_algorithm, measure_weight_dict, algorithm_portfolio) for discovery_algorithm in algorithm_portfolio}
    return ret


def predicted_regression_based_scalarization(log_path_to_predict, regression_method, measure_weight_dict, ready_training, feature_portfolio, algorithm_portfolio):
    ret = {discovery_algorithm: predicted_regression_based_combined_score_of_discovery_algorithm(log_path_to_predict, discovery_algorithm, regression_method,
                                                                                                 measure_weight_dict, ready_training, feature_portfolio, algorithm_portfolio) for discovery_algorithm in algorithm_portfolio}
    return ret


def actual_regression_based_scalarization(log_path_to_predict, measure_weight_dict, algorithm_portfolio):
    ret = {discovery_algorithm: actual_regression_based_combined_score_of_discovery_algorithm(
        log_path_to_predict, discovery_algorithm, measure_weight_dict) for discovery_algorithm in algorithm_portfolio}
    return ret


def predicted_classification(log_path, classification_method, measure_name, ready_training, feature_portfolio, algorithm_portfolio):

    if is_regression_based_classification_method_string(classification_method):
        return regression_based_classification(
            log_path, classification_method, measure_name, ready_training, feature_portfolio, algorithm_portfolio)

    ret = read_fitted_classifier(
        classification_method, measure_name, ready_training, feature_portfolio)
    clf = ret

    predictions = clf.predict(read_feature_vector(log_path, feature_portfolio))

    return predictions[0]


if __name__ == "__main__":
    # shap.initjs()
    fix_corrupt_cache()
    globals.algorithm_portfolio = ["alpha", "heuristic",
                                   "inductive", "ILP", "split"]

    globals.algorithm_portfolio = [
        "alpha", "inductive", "heuristic", "split", "ILP"]
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
    all_logs = gather_all_xes("../logs/testing") + gather_all_xes(
        "../logs/training") + gather_all_xes("../logs/modified_eventlogs")
    algorithm_portfolio = globals.algorithm_portfolio

    # merge get_all_ready_logs and init_given_parameters
    ready_logs = get_all_ready_logs(
        all_logs, feature_list, algorithm_portfolio, globals.measures_list)

    classification_method = "xgboost"
    measure_name1 = "token_fitness"
    measure_name2 = "token_precision"

    init_given_parameters(ready_logs, algorithm_portfolio,
                          feature_list, globals.measures_list)
    measure_weight_dict = {measure: 0 for measure in globals.measures_list}
    measure_weight_dict[measure_name1] = 1
    measure_weight_dict[measure_name2] = 1

    regression_method = "random_forest"
    for log_path_to_predict in ready_logs:
        actual_classification_ = actual_classification_based_scalarization(
            log_path_to_predict, measure_weight_dict, algorithm_portfolio)
        predicted_classification_ = predicted_classification_based_scalarization(
            log_path_to_predict, classification_method, measure_weight_dict, ready_logs, feature_list, algorithm_portfolio)
        actual_regression_ = actual_regression_based_scalarization(
            log_path_to_predict, measure_weight_dict, algorithm_portfolio)
        predicted_regression_ = predicted_regression_based_scalarization(
            log_path_to_predict, regression_method, measure_weight_dict, ready_logs, feature_list, algorithm_portfolio)

        print("classification")
        input(f"classification actual {actual_classification_}")
        input(f"classification predicted {predicted_classification_}")

        print("regression")
        input(f"regression actual {actual_regression_}")
        input(f"regression predicted {predicted_regression_}")
