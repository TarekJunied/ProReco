import sys
import shutil
from sklearn.model_selection import train_test_split
import random
import copy
import matplotlib.pyplot as plt
import numpy as np
import time
import os
import numpy as np
import globals
from datetime import datetime
from sklearn.metrics import accuracy_score, mean_squared_error
from utils import get_all_ready_logs, load_cache_variable
from recommender import classification, regression, predict_regression, compute_fitted_classifier
from filehelper import gather_all_xes, get_all_ready_logs_multiple
from measures import read_target_entries, read_classification_target_vector,  read_worst_entry, read_measure_entry, read_target_entry
from feature_controller import read_feature_matrix, read_single_feature, get_total_feature_functions_dict
from feature_selection import select_k_best_features, read_optimal_features
from flask_app.features.removed_features import get_removed_features_list
from init import init_given_parameters
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
import os
from datetime import datetime
import time

# modified for choosing features


def create_scikit_classification_evaluation_plot(selected_measures, ready_training, ready_testing, classification_method, feature_portfolio, plot_title):
    values = []
    categories = selected_measures
    display_str = ""

    total_accuracy = 0
    for measure in selected_measures:
        display_str += f" {len(ready_testing)} "
        cur_measure_accuracy = evaluate_scikit_measure_accuracy(
            measure, ready_training, ready_testing, classification_method, feature_portfolio)
        values += [cur_measure_accuracy]
        total_accuracy += cur_measure_accuracy

    average_accuracy = total_accuracy / \
        len(selected_measures)  # Calculate average accuracy

    plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
    plt.bar(categories, values, color='royalblue')
    plt.axhline(y=average_accuracy, color='red', linestyle='-',
                linewidth=1.5, label='Average Accuracy')
    plt.text(len(categories)-1, average_accuracy,
             f'Avg: {average_accuracy:.2f}', color='red', va='bottom')
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title(display_str)

    # Set y-axis ticks and limits
    plt.yticks([i/10 for i in range(11)])
    plt.ylim(0, 1)

    for i in range(1, 10):
        plt.axhline(y=i/10, color='gray', linestyle='--', linewidth=0.5)

    plt.grid(True, axis='y', linestyle='--',
             alpha=0.7)  # Add a horizontal grid
    plt.xticks(rotation=90)

    now = datetime.now()

    # Format the current date as a string
    current_date_string = now.strftime("%Y-%m-%d")

    storage_dir = f"../evaluation/accuracy_tests/scikit_{current_date_string}"

    if not os.path.exists(storage_dir):
        # If it doesn't exist, create the directory
        os.mkdir(storage_dir)

    plt.savefig(
        f'{storage_dir}/{plot_title}_{classification_method}_accuracy_{int(time.time())}.png', dpi=300, bbox_inches='tight')


def evaluate_scikit_measure_accuracy(measure, ready_training, ready_testing, classification_method, feature_portfolio):

    y_true = [None] * len(ready_testing)
    y_pred = [None] * len(ready_testing)

    for i in range(len(ready_testing)):
        y_true[i] = read_target_entry(
            ready_testing[i], measure, globals.algorithm_portfolio)
        y_pred[i] = classification(
            ready_testing[i],  classification_method, measure, ready_training, feature_portfolio)

    return accuracy_score(y_true, y_pred)


def create_two_measure_graph(measure_name1, measure_name2, discovery_algorithm):
    original_logpaths = gather_all_xes(
        "../logs/training") + gather_all_xes("../logs/testing")
    full_logs = set(get_all_ready_logs(original_logpaths, measure_name1
                                       )).intersection(set(get_all_ready_logs(original_logpaths, measure_name2)))

    full_logs = list(full_logs)
    x_values = []
    y_values = []

    for log_path in full_logs:
        x_values += [read_measure_entry(log_path,
                                        discovery_algorithm, measure_name1)]
        y_values += [read_measure_entry(log_path,
                                        discovery_algorithm, measure_name2)]

    # Plotting the points
    plt.scatter(x_values, y_values, color='red', label='Points', s=2)

    # Adding labels and title
    plt.xlabel(measure_name1)
    plt.ylabel(measure_name2)
    plt.title(
        f"{measure_name1} vs {measure_name2} with {discovery_algorithm} and {len(x_values)} values")

    # Display the legend
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    now = datetime.now()

    current_date_string = now.strftime("%Y-%m-%d")

    if not os.path.exists(f"../evaluation/measure_comparisons_{current_date_string}"):
        # If it doesn't exist, create the directory
        os.mkdir(f"../evaluation/measure_comparisons_{current_date_string}")

    plt.savefig(
        f"../evaluation/measure_comparisons_{current_date_string}/{discovery_algorithm}_{measure_name1}_{measure_name2}_{int(time.time())}.png", dpi=300, bbox_inches='tight')


def split_log_paths(log_paths, train_percent=0.7):
    # Randomly shuffle the list of log paths
    random.shuffle(log_paths)

    # Calculate the split index
    split_index = int(len(log_paths) * train_percent)

    # Split the list into training and testing sets
    train_paths = log_paths[:split_index]
    test_paths = log_paths[split_index:]

    return train_paths, test_paths


def create_scikit_classification_evaluation_plot_with_k_feature_selection(selected_measures, ready_training, ready_testing, k, classification_method, feature_portfolio, plot_title):
    values = []
    categories = selected_measures
    display_str = ""

    total_accuracy = 0
    for measure in selected_measures:
        globals.selected_features = select_k_best_features(
            ready_training+ready_testing, globals.algorithm_portfolio, globals.selected_features, measure, k=k)
        display_str += f" {len(ready_testing)} "
        cur_measure_accuracy = evaluate_scikit_measure_accuracy(
            measure, ready_training, ready_testing, classification_method, feature_portfolio)
        values += [cur_measure_accuracy]
        total_accuracy += cur_measure_accuracy

    average_accuracy = total_accuracy / \
        len(selected_measures)  # Calculate average accuracy

    plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
    plt.bar(categories, values, color='royalblue')
    plt.axhline(y=average_accuracy, color='red', linestyle='-',
                linewidth=1.5, label='Average Accuracy')
    plt.text(len(categories)-1, average_accuracy,
             f'Avg: {average_accuracy:.2f}', color='red', va='bottom')
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title(display_str)

    # Set y-axis ticks and limits
    plt.yticks([i/10 for i in range(11)])
    plt.ylim(0, 1)

    for i in range(1, 10):
        plt.axhline(y=i/10, color='gray', linestyle='--', linewidth=0.5)

    plt.grid(True, axis='y', linestyle='--',
             alpha=0.7)  # Add a horizontal grid
    plt.xticks(rotation=90)

    now = datetime.now()

    # Format the current date as a string
    current_date_string = now.strftime("%Y-%m-%d")

    storage_dir = f"../evaluation/accuracy_tests/scikit_{current_date_string}"

    if not os.path.exists(storage_dir):
        # If it doesn't exist, create the directory
        os.mkdir(storage_dir)

    plt.savefig(
        f'{storage_dir}/{plot_title}_{classification_method}_accuracy_{int(time.time())}.png', dpi=300, bbox_inches='tight')


def create_scikit_classification_evaluation_plot_with_optimal_feature_selection(selected_measures, ready_training, ready_testing, classification_method, plot_title):
    values = []
    categories = selected_measures
    display_str = ""

    total_accuracy = 0
    feature_portfolio = copy.deepcopy(globals.selected_features)
    for measure in selected_measures:
        measure_optimized_feature_portfolio = read_optimal_features(
            ready_training+ready_testing, classification_method, measure, feature_portfolio, globals.algorithm_portfolio)
        display_str += f" {len(ready_testing)} "
        cur_measure_accuracy = evaluate_scikit_measure_accuracy(
            measure, ready_training, ready_testing, classification_method, measure_optimized_feature_portfolio)
        values += [cur_measure_accuracy]
        total_accuracy += cur_measure_accuracy

    average_accuracy = total_accuracy / \
        len(selected_measures)  # Calculate average accuracy

    plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
    plt.bar(categories, values, color='royalblue')
    plt.axhline(y=average_accuracy, color='red', linestyle='-',
                linewidth=1.5, label='Average Accuracy')
    plt.text(len(categories)-1, average_accuracy,
             f'Avg: {average_accuracy:.2f}', color='red', va='bottom')
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title(display_str)

    # Set y-axis ticks and limits
    plt.yticks([i/10 for i in range(11)])
    plt.ylim(0, 1)

    for i in range(1, 10):
        plt.axhline(y=i/10, color='gray', linestyle='--', linewidth=0.5)

    plt.grid(True, axis='y', linestyle='--',
             alpha=0.7)  # Add a horizontal grid
    plt.xticks(rotation=90)

    now = datetime.now()

    # Format the current date as a string
    current_date_string = now.strftime("%Y-%m-%d")

    storage_dir = f"../evaluation/accuracy_tests/scikit_{current_date_string}"

    if not os.path.exists(storage_dir):
        # If it doesn't exist, create the directory
        os.mkdir(storage_dir)

    plt.savefig(
        f'{storage_dir}/{plot_title}_{classification_method}_accuracy_{int(time.time())}.png', dpi=300, bbox_inches='tight')


def clear_cached_classifiers():
    classifiers_dir = "./classifiers/"
    folder_path = classifiers_dir
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


if __name__ == "__main__":
    sys.setrecursionlimit(5000)

    clear_cached_classifiers()
    globals.algorithm_portfolio = [
        "alpha", "inductive", "heuristic", "split", "ILP"]
    feature_dict = get_total_feature_functions_dict()

    feature_list = list(feature_dict.keys())

    globals.selected_features = feature_list
    globals.measures_list = ["token_fitness", "token_precision",
                             "no_total_elements", "generalization", "pm4py_simplicity"]

    globals.classification_methods = [
        x for x in globals.classification_methods if x not in ["knn", "svm"]]
    ready_logs = get_all_ready_logs_multiple(gather_all_xes("../logs/training") + gather_all_xes("../logs/testing")
                                             + gather_all_xes("../logs/modified_eventlogs"))

    init_given_parameters(ready_logs,
                          globals.algorithm_portfolio, feature_list, globals.measures_list)

    ready_training, ready_testing = split_log_paths(ready_logs)
    for classification_method in globals.classification_methods:
        for measure in globals.measures_list:
            read_optimal_features(ready_logs, classification_method, measure,
                                  globals.selected_features, globals.algorithm_portfolio, cv=5, scoring='accuracy')

    for no_of_features in [10, 20, 50, 150, len(feature_list)]:
        clear_cached_classifiers()
        globals.selected_features = feature_list
        for classification_method in globals.classification_methods:
            create_scikit_classification_evaluation_plot_with_k_feature_selection(
                globals.measures_list, ready_training, ready_testing, no_of_features, classification_method, globals.selected_features, f"like_before_{no_of_features}_features_all_logs_cached_clf")

    globals.selected_features = feature_list

    clear_cached_classifiers()

    for classification_method in globals.classification_methods:
        create_scikit_classification_evaluation_plot_with_optimal_feature_selection(
            globals.measures_list, ready_training, ready_testing, classification_method,  f"optimal_features_all_logs_cached_clf")
