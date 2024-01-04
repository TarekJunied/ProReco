
import matplotlib.pyplot as plt
import math
import pandas as pd
import globals
import numpy as np
import subprocess
import os
import pm4py
from xgboost import XGBClassifier
from filehelper import gather_all_xes, get_all_ready_logs
from feature_controller import read_feature_matrix, read_feature_vector, read_single_feature
from measures import read_measure_entry, read_regression_target_vector, read_target_entry
from init import *
from classifiers import read_fitted_classifier
from regressors import regression_based_classification, regression
from sklearn.tree import plot_tree


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
                                   discovery_algorithm, measure, ready_training)
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

    ret = {discovery_algorithm: round(predicted_regression_based_combined_score_of_discovery_algorithm(log_path_to_predict, discovery_algorithm, regression_method,
                                                                                                       measure_weight_dict, ready_training, feature_portfolio, algorithm_portfolio), 2) for discovery_algorithm in algorithm_portfolio}
    return ret


def actual_regression_based_scalarization(log_path_to_predict, measure_weight_dict, algorithm_portfolio):
    ret = {discovery_algorithm: actual_regression_based_combined_score_of_discovery_algorithm(
        log_path_to_predict, discovery_algorithm, measure_weight_dict) for discovery_algorithm in algorithm_portfolio}
    return ret


if __name__ == "__main__":
    # shap.initjs()
    fix_corrupt_cache()
    globals.algorithm_portfolio = ["alpha", "heuristic",
                                   "inductive", "ILP", "split"]

    globals.algorithm_portfolio = [
        "alpha", "inductive", "heuristic", "split", "ILP"]
    feature_dict = get_total_feature_functions_dict()

    feature_list = list(feature_dict.keys())

    globals.feature_portfolio = feature_list
    globals.measure_portfolio = ["token_fitness", "token_precision",
                                 "no_total_elements", "generalization", "pm4py_simplicity"]
