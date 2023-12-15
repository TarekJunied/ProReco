import sys
import psutil
import matplotlib.pyplot as plt
import numpy as np
import time
import os
import numpy as np
import globals
from datetime import datetime
from sklearn.metrics import accuracy_score, mean_squared_error
from utils import get_all_ready_logs,load_cache_variable
from recommender import classification,regression, predict_regression
from filehelper import gather_all_xes, get_all_ready_logs_multiple
from measures import read_target_entries, read_classification_target_vector,  read_worst_entry,read_measure_entry, read_target_entry
from features import read_feature_matrix,read_single_feature
from init import init


def create_scikit_classification_evaluation_plot(selected_measures,ready_training,ready_testing, classification_method="knn",):
    values = []
    categories = selected_measures
    display_str = ""


    for measure in selected_measures:
    
        display_str += f" {len(ready_testing)} "
        values += [evaluate_scikit_measure_accuracy(measure,ready_training,ready_testing,classification_method)]



    plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
    plt.bar(categories, values, color='royalblue')
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title(display_str)

    # Set y-axis ticks and limits
    plt.yticks([i/10 for i in range(11)])
    plt.ylim(0, 1)

    for i in range(1, 10):
        plt.axhline(y=i/10, color='gray', linestyle='--', linewidth=0.5)

    plt.grid(True, axis='y', linestyle='--', alpha=0.7)  # Add a horizontal grid
    plt.xticks(rotation=90)

    now = datetime.now()

    # Format the current date as a string
    current_date_string = now.strftime("%Y-%m-%d")

    if not os.path.exists(f"../evaluation/scikit_{current_date_string}"):
    # If it doesn't exist, create the directory
        os.mkdir(f"../evaluation/scikit_{current_date_string}")

    plt.savefig(f'../evaluation/scikit_{current_date_string}/{classification_method}_accuracy_{int(time.time())}.png', dpi=300, bbox_inches='tight')



def evaluate_scikit_measure_accuracy(measure,ready_training,ready_testing, classification_method):


    y_true = [None] * len(ready_testing)
    y_pred = [None] * len(ready_testing)

    for i in range(len(ready_testing)):
        y_true[i] = read_target_entry(ready_testing[i], measure)
        y_pred[i] = classification(ready_testing[i],  classification_method,measure,ready_training)


    return accuracy_score(y_true, y_pred)



def create_two_measure_graph(measure_name1,measure_name2,discovery_algorithm):
    original_logpaths = gather_all_xes("../logs/training") + gather_all_xes("../logs/testing")
    full_logs = set(get_all_ready_logs(original_logpaths,measure_name1
                                  )).intersection(set(get_all_ready_logs(original_logpaths,measure_name2)))
    
    full_logs = list(full_logs)
    x_values = []
    y_values = []

    for log_path in full_logs:
            x_values +=[read_measure_entry(log_path,discovery_algorithm,measure_name1)]
            y_values +=[read_measure_entry(log_path,discovery_algorithm,measure_name2)]

    # Plotting the points
    plt.scatter(x_values, y_values, color='red', label='Points', s=2)

    # Adding labels and title
    plt.xlabel(measure_name1)
    plt.ylabel(measure_name2)
    plt.title(f"{measure_name1} vs {measure_name2} with {discovery_algorithm} and {len(x_values)} values")

    # Display the legend
    plt.xlim(0, 1)
    plt.ylim(0, 1)


    now = datetime.now()

    current_date_string = now.strftime("%Y-%m-%d")

    if not os.path.exists(f"../evaluation/measure_comparisons_{current_date_string}"):
    # If it doesn't exist, create the directory
        os.mkdir(f"../evaluation/measure_comparisons_{current_date_string}")

    plt.savefig(f"../evaluation/measure_comparisons_{current_date_string}/{discovery_algorithm}_{measure_name1}_{measure_name2}_{int(time.time())}.png", dpi=300, bbox_inches='tight')

def create_scikit_regression_evaluation_plot(measure_name, discovery_algorithm):
    """create one bar for each regression method

    Args:
        measure_name: _description_
        discovery_algorithm: _description_
    """

    values = []
    categories = globals.regression_methods
    display_str = ""

    ready_testing  = list(globals.testing_log_paths.keys())

    for regression_method in categories:
        values+=[evaluate_scikit_measure_rmse(measure_name,regression_method,discovery_algorithm)]




    plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
    plt.bar(categories, values, color='royalblue')
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title(display_str)


    for i in range(1, 10):
        plt.axhline(y=i/10, color='gray', linestyle='--', linewidth=0.5)

    plt.grid(True, axis='y', linestyle='--', alpha=0.7)  # Add a horizontal grid
    plt.xticks(rotation=90)



    if not os.path.exists(f"../evaluation/{discovery_algorithm}"):
    # If it doesn't exist, create the directory
        os.mkdir(f"../evaluation/{discovery_algorithm}")

    plt.savefig(f"../evaluation/{discovery_algorithm}/{measure_name}_scikit_{int(time.time())}.png", dpi=300, bbox_inches='tight')







def evaluate_scikit_measure_rmse(measure, regression_method,discovery_algorithm):
    ready_testing = list(globals.testing_log_paths.keys())

    y_true = []
    y_pred = []

    ready_training = get_all_ready_logs(gather_all_xes("../logs/training"),measure)
    for log_path in ready_testing:
        y_true.append(read_measure_entry(log_path,discovery_algorithm, measure))
        y_pred.append(regression(log_path, regression_method, measure,discovery_algorithm, ready_training))  # Assuming ready_training is available

    return mean_squared_error(y_true, y_pred, squared=False)  # Using squared=False to get RMSE


def create_scikit_regression_evaluation_plot(selected_measures, regression_method="linear_regression"):
    values = []
    categories = selected_measures
    display_str = ""

    ready_testing  = list(globals.testing_log_paths.keys())


    for measure in selected_measures:
    
        display_str += f" {len(ready_testing)} "
        values += [evaluate_scikit_regression_based_prediction_measure_accuracy(measure,regression_method)]




    plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
    plt.bar(categories, values, color='royalblue')
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title(display_str)

    # Set y-axis ticks and limits
    plt.yticks([i/10 for i in range(11)])
    plt.ylim(0, 1)

    for i in range(1, 10):
        plt.axhline(y=i/10, color='gray', linestyle='--', linewidth=0.5)

    plt.grid(True, axis='y', linestyle='--', alpha=0.7)  # Add a horizontal grid
    plt.xticks(rotation=90)

    now = datetime.now()

    # Format the current date as a string
    current_date_string = now.strftime("%Y-%m-%d")

    plot_dir  = f"../evaluation/regression_cikit_{current_date_string}"
    if not os.path.exists(plot_dir):
    # If it doesn't exist, create the directory
        os.mkdir(plot_dir)

    plt.savefig(f'{plot_dir}/{regression_method}_{int(time.time())}.png', dpi=300, bbox_inches='tight')


def evaluate_scikit_regression_based_prediction_measure_accuracy(measure,regression_method):

    ready_testing = list(globals.testing_log_paths.keys())

    y_true = [None] * len(ready_testing)
    y_pred = [None] * len(ready_testing)

    for i in range(len(ready_testing)):
        y_true[i] = read_target_entry(ready_testing[i], measure)
        y_pred[i] = predict_regression(ready_testing[i], measure,  regression_method)


    return accuracy_score(y_true, y_pred)


def create_auto_regression_accuracy_plot(selected_measures):
    values = []
    categories = selected_measures
    display_str = ""

    ready_testing  = list(globals.testing_log_paths.keys())


    for measure in selected_measures:
    
        display_str += f" {len(ready_testing)} "
        max_val = max([evaluate_scikit_regression_based_prediction_measure_accuracy(measure,regression_method) for regression_method in globals.regression_methods])
        values += [max_val]




    plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
    plt.bar(categories, values, color='royalblue')
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title(display_str)

    # Set y-axis ticks and limits
    plt.yticks([i/10 for i in range(11)])
    plt.ylim(0, 1)

    for i in range(1, 10):
        plt.axhline(y=i/10, color='gray', linestyle='--', linewidth=0.5)

    plt.grid(True, axis='y', linestyle='--', alpha=0.7)  # Add a horizontal grid
    plt.xticks(rotation=90)

    now = datetime.now()

    # Format the current date as a string
    current_date_string = now.strftime("%Y-%m-%d")

    plot_dir  = f"../evaluation/regression_cikit_{current_date_string}"
    if not os.path.exists(plot_dir):
    # If it doesn't exist, create the directory
        os.mkdir(plot_dir)

    regression_method = "automl"
    plt.savefig(f'{plot_dir}/{regression_method}_{int(time.time())}.png', dpi=300, bbox_inches='tight')



if __name__ == "__main__":
    sys.setrecursionlimit(5000)

    #init()
    measures_list = ["token_fitness",  "token_precision",
                              "generalization", "pm4py_simplicity"]
    


    ready_training = get_all_ready_logs_multiple(gather_all_xes("../logs/training"))
    ready_testing = get_all_ready_logs_multiple(gather_all_xes("../logs/testing"))


    create_scikit_classification_evaluation_plot(globals.measures_list,ready_training, ready_testing, "autofolio")
    #for classification_method in globals.classification_methods:
    #    create_scikit_classification_evaluation_plot(globals.measures_list,ready_training,ready_testing,classification_method)

  

    """"


    for i in range(len(measures_list)):
        for j in range(i+1, len(measures_list)):
                measure_name1 = measures_list[i]
                measure_name2 = measures_list[j]
                for discovery_algorithm in globals.algorithm_portfolio:
                    create_two_measure_graph(measure_name1,measure_name2,discovery_algorithm)
    """

