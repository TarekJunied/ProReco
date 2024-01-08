import sys
from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import os
import numpy as np
import globals
from datetime import datetime
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error
from utils import load_cache_variable, split_data, get_log_name, read_log
from filehelper import gather_all_xes, get_all_ready_logs, clear_cached_classifiers, clear_cached_regressors, clear_cached_binary_classifiers
from measures import read_measure_entry, read_target_entry, read_binary_classification_target_entry, read_regression_target_vector
from feature_controller import read_feature_matrix, read_single_feature, get_total_feature_functions_dict
from regressors import get_regression_based_classification_methods, regression, regression_based_classification, init_regressors
from classifiers import classification
from multiobjective import predicted_regression_based_scalarization, actual_regression_based_scalarization
from flask_app.features.removed_features import get_removed_features_list
from init import init_given_parameters, filter_instances_with_nan, reset_all_cached_predictors
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
import os
from datetime import datetime
import time


def evaluate_mo_scikit_measure_accuracy(measure_weights_dict, ready_testing, regression_method):
    y_pred = []
    y_true = []
    for log_path in ready_testing:
        predicted_scores_dict = predicted_regression_based_scalarization(
            log_path, regression_method, measure_weights_dict, [], globals.feature_portfolio, globals.algorithm_portfolio)
        actual_scores_dict = actual_regression_based_scalarization(
            log_path, measure_weights_dict, globals.algorithm_portfolio)
        predicted_best_algo = max(
            predicted_scores_dict, key=predicted_scores_dict.get)
        actual_best_algo = max(actual_scores_dict, key=actual_scores_dict.get)
        y_pred += [predicted_best_algo]
        y_true += [actual_best_algo]

    return accuracy_score(y_true, y_pred)


def mo_min_max_single_point_accuracy(actual_dict, predicted_dict):

    best_actual_algo = max(actual_dict, key=actual_dict.get)
    worst_actual_algo = min(actual_dict, key=actual_dict.get)

    best_predicted_algo = max(predicted_dict, key=predicted_dict.get)

    if best_predicted_algo == worst_actual_algo:
        accuracy = 0
    else:
        # Using min-max normalization to calculate accuracy
        predicted_value = predicted_dict[best_predicted_algo]
        worst_value = actual_dict[worst_actual_algo]
        best_value = actual_dict[best_actual_algo]

        # Ensure the denominator is not zero
        if best_value != worst_value:
            accuracy = (predicted_value - worst_value) / \
                (best_value - worst_value)
            # Ensuring accuracy is between 0 and 1
            accuracy = max(0, min(accuracy, 1))
        else:
            # If the worst and best actual performance are the same, can't compute as usual
            accuracy = 0  # or some other rule as defined by system requirements

    return accuracy


def evaluate_mo_min_max_measure_accuracy(measure_weights_dict, ready_testing, regression_method):

    accuracy_sum = 0
    for log_path in ready_testing:
        predicted_scores_dict = predicted_regression_based_scalarization(
            log_path, regression_method, measure_weights_dict, [], globals.feature_portfolio, globals.algorithm_portfolio)
        actual_scores_dict = actual_regression_based_scalarization(
            log_path, measure_weights_dict, globals.algorithm_portfolio)
        accuracy_sum += mo_min_max_single_point_accuracy(
            actual_scores_dict, predicted_scores_dict)

    return accuracy_sum/len(ready_testing)


def evaluate_scikit_measure_accuracy(measure, ready_testing, classification_method):
    feature_portfolio = globals.feature_portfolio

    y_true = [read_target_entry(
        log_path, measure, globals.algorithm_portfolio) for log_path in ready_testing]
    y_pred = [classification(log_path,  classification_method, measure, [],
                             feature_portfolio) for log_path in ready_testing]

    return accuracy_score(y_true, y_pred)


def create_measure_bar_plot(selected_measures, y_label, values, plot_title):

    total_val = sum(values)

    average_val = total_val / \
        len(selected_measures)  # Calculate average accuracy

    plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
    plt.bar(selected_measures, values, color='royalblue')
    plt.axhline(y=average_val, color='red', linestyle='-',
                linewidth=1.5, label=f'Average Accuracy')
    plt.text(len(selected_measures)-1, average_val,
             f'Avg: {average_val:.2f}', color='red', va='bottom')
    plt.xlabel('Measures')
    plt.ylabel(y_label)
    plt.title(plot_title)

    # Set y-axis ticks and limits
    plt.yticks([i/10 for i in range(11)])
    plt.ylim(0, 1)

    for i in range(1, 10):
        plt.axhline(y=i/10, color='gray', linestyle='--', linewidth=0.5)

    plt.grid(True, axis='y', linestyle='--',
             alpha=0.7)  # Add a horizontal grid
    plt.xticks(rotation=90)

    current_date = datetime.now()

    # Format the date to YYYY_MM_DD format
    formatted_date = current_date.strftime('%Y_%m_%d')

    storage_dir = f"../evaluation/{formatted_date}/accuracy_plots"
    os.makedirs(storage_dir, exist_ok=True)

    plt.savefig(
        f'{storage_dir}/{plot_title}.png', dpi=300, bbox_inches='tight')

    plt.close()


def create_scikit_regression_based_classification_evaluation_plot(selected_measures, ready_testing, regression_method, plot_title, accuracy_measure="own"):

    if accuracy_measure == "own":
        values = [evaluate_min_max_measure_accuracy(measure, ready_testing, regression_method)
                  for measure in selected_measures]
    else:
        values = [evaluate_scikit_measure_accuracy(measure, ready_testing, f"regression_based_{regression_method}")
                  for measure in selected_measures]

    create_measure_bar_plot(
        selected_measures, f"Accuracy {len(ready_testing)}", values, plot_title)


def create_scikit_regression_mae_evaluation_plot(selected_measures, ready_testing, regression_method, plot_title):
    values = [evaluate_scikit_measure_mae(measure, ready_testing, regression_method)
              for measure in selected_measures]

    create_measure_bar_plot(
        selected_measures, f"MAE {len(ready_testing)}", values, plot_title)


def evaluate_scikit_measure_mae(measure,  ready_testing, regression_method):
    algorithm_portfolio = globals.algorithm_portfolio

    y_true = [read_measure_entry(log_path, discovery_algorithm, measure)
              for log_path in ready_testing for discovery_algorithm in algorithm_portfolio]
    y_pred = [regression(log_path, regression_method, discovery_algorithm, measure, [])
              for log_path in ready_testing for discovery_algorithm in algorithm_portfolio]
    return mean_absolute_error(y_true, y_pred)


def create_algorithm_x_measure_heatmap(all_logs, plot_title):
    rows = globals.algorithm_portfolio
    columns = globals.measure_portfolio + ["average"]
    value_array = np.empty((len(rows), len(columns)))
    for i in range(len(rows)):
        for j in range(len(columns)):
            if j < len(columns) - 1:
                current_value_list = [read_measure_entry(
                    log_path, rows[i], columns[j]) for log_path in all_logs]
                value_array[i, j] = sum(
                    current_value_list)/len(current_value_list)
            else:
                value_array[i, j] = sum(
                    [value_array[i, k] for k in range(j)]) / len(globals.measure_portfolio)

    heatmap_data = pd.DataFrame(value_array, index=rows, columns=columns)

    # Create the heatmap using seaborn
    plt.figure(figsize=(10, 8))  # Adjust the figure size as needed
    sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="YlGnBu")
    # Add a title to the heatmap
    plt.title('Heatmap of Discovery Algorithms Performance')
    storage_dir = "../evaluation/algorithm_heatmap"
    os.makedirs(storage_dir, exist_ok=True)
    plt.savefig(f"{storage_dir}/{plot_title}.png")
    plt.close()


def so_min_max_single_point_accuracy(log_path, regression_method, measure_name):
    predicted_dict = {algo: regression(log_path, regression_method, algo, measure_name, [])
                      for algo in globals.algorithm_portfolio}
    actual_dict = {algo: read_measure_entry(log_path, algo, measure_name)
                   for algo in globals.algorithm_portfolio}

    best_actual_algo = max(actual_dict, key=actual_dict.get)
    worst_actual_algo = min(actual_dict, key=actual_dict.get)

    best_predicted_algo = max(predicted_dict, key=predicted_dict.get)

    if best_predicted_algo == worst_actual_algo:
        accuracy = 0
    else:
        # Using min-max normalization to calculate accuracy
        predicted_value = predicted_dict[best_predicted_algo]
        worst_value = actual_dict[worst_actual_algo]
        best_value = actual_dict[best_actual_algo]

        # Ensure the denominator is not zero
        if best_value != worst_value:
            accuracy = (predicted_value - worst_value) / \
                (best_value - worst_value)
            # Ensuring accuracy is between 0 and 1
            accuracy = max(0, min(accuracy, 1))
        else:
            # If the worst and best actual performance are the same, can't compute as usual
            accuracy = 0  # or some other rule as defined by system requirements

    return accuracy


def create_scikit_regression_mae_evaluation_plot(selected_measures, ready_testing, regression_method, plot_title):
    values = [evaluate_scikit_measure_mae(measure, ready_testing, regression_method)
              for measure in selected_measures]

    create_measure_bar_plot(
        selected_measures, f"MAE {len(ready_testing)}", values, plot_title)


def create_scikit_scatter_plot(y_true, y_pred, plot_title):
    plt.scatter(y_true, y_pred)
    plt.title('Scatter plot of Actual vs. Predicted')
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')

    # Add a reference line
    # k-- is for black dashed line, lw is line width
    plt.plot([0, 1], [0, 1], 'k--', lw=2)

    plt.show()
    current_date = datetime.now()

    # Format the date to YYYY_MM_DD format
    formatted_date = current_date.strftime('%Y_%m_%d')

    storage_dir = f"../evaluation/{formatted_date}/scatter_plots"
    os.makedirs(storage_dir, exist_ok=True)

    plt.savefig(
        f'{storage_dir}/scatter_plot_{plot_title}.png', dpi=300, bbox_inches='tight')

    plt.close()


def create_scikit_regression_scatter_plot(measure, regression_method, ready_testing, plot_title):

    y_true = [read_measure_entry(log_path, discovery_algorithm, measure)
              for log_path in ready_testing for discovery_algorithm in globals.algorithm_portfolio]
    y_pred = [regression(log_path, regression_method, discovery_algorithm, measure, [])
              for log_path in ready_testing for discovery_algorithm in globals.algorithm_portfolio]

    create_scikit_scatter_plot(y_true, y_pred, plot_title)


def evaluate_min_max_measure_accuracy(measure, ready_testing, regression_method):

    accuracy_sum = 0
    for i in range(len(ready_testing)):
        accuracy_sum += so_min_max_single_point_accuracy(
            ready_testing[i], regression_method, measure)

    return accuracy_sum / len(ready_testing)


def get_regressors_accuracy(ready_testing, regression_method, discovery_algorithm, measure_name):

    y_true = [read_measure_entry(
        log_path, discovery_algorithm, measure_name) for log_path in ready_testing]
    y_pred = [regression(log_path, regression_method, discovery_algorithm, measure_name, [])
              for log_path in ready_testing]

    return mean_absolute_error(y_true, y_pred)


def mse_mae_computation(ready_testing, regression_method, discovery_algorithm, measure):
    y_true = [read_measure_entry(
        log_path, discovery_algorithm, measure) for log_path in ready_testing]
    y_pred = [regression(log_path, regression_method, discovery_algorithm, measure, [])
              for log_path in ready_testing]
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    return mse, mae


def string_encoding_of_measure_weights_dict(measure_weights_dict):
    ret = ""
    if measure_weights_dict['token_fitness'] > 0:
        ret += f"f {measure_weights_dict['token_fitness']} "
    if measure_weights_dict['token_precision'] > 0:
        ret += f"p {measure_weights_dict['token_precision']} "
    if measure_weights_dict['pm4py_simplicity'] > 0:
        ret += f"s {measure_weights_dict['pm4py_simplicity']} "
    if measure_weights_dict['pm4py_simplicity'] > 0:
        ret += f"g {measure_weights_dict['pm4py_simplicity']}"
    return ret


if __name__ == "__main__":
    sys.setrecursionlimit(5000)

    all_logs = gather_all_xes("../logs")
    ready_logs = get_all_ready_logs(
        all_logs, globals.feature_portfolio, globals.algorithm_portfolio, globals.measure_portfolio)
    ready_training, ready_testing = split_data(ready_logs)

    init_given_parameters(ready_logs, globals.algorithm_portfolio,
                          globals.feature_portfolio, globals.measure_portfolio)
    # CHANGE IT TO ONLY LOAD NEEDED FEATURES, ONCE OPTIMAL FEATURE SETS ARE COMPUTED DO THAT
    no_cv = 5
    measure_weights_dict_list = [{"token_fitness": 0.5, "token_precision": 0.5, "pm4py_simplicity": 0, "generalization": 0},
                                 {"token_fitness": 0.5, "token_precision": 0,
                                  "pm4py_simplicity": 0.5, "generalization": 0},
                                 {"token_fitness": 0.5, "token_precision": 0,
                                  "pm4py_simplicity": 0, "generalization": 0.5},
                                 {"token_fitness": 0, "token_precision": 0.5,
                                  "pm4py_simplicity": 1, "generalization": 0},
                                 {"token_fitness": 0, "token_precision": 1,
                                  "pm4py_simplicity": 0.5, "generalization": 0},
                                 {"token_fitness": 0, "token_precision": 0.75,
                                  "pm4py_simplicity": 1, "generalization": 0},
                                 {"token_fitness": 0, "token_precision": 1,
                                  "pm4py_simplicity": 0, "generalization": 0.75},
                                 {"token_fitness": 0, "token_precision": 0,
                                  "pm4py_simplicity": 1, "generalization": 1}]

    created_scatter_plot = {
        regression_method: False for regression_method in globals.regression_methods}
    for regression_method in globals.regression_methods:
        single_objective_min_max_accuracy_dict = {measure: []
                                                  for measure in globals.measure_portfolio}
        single_objective_scikit_accuracy_dict = {measure: []
                                                 for measure in globals.measure_portfolio}
        multi_objective_min_max_accuracy_dict = {str(measure_weights_dict): []
                                                 for measure_weights_dict in measure_weights_dict_list}
        multi_objective_scikit_accuracy_dict = {str(measure_weights_dict): []
                                                for measure_weights_dict in measure_weights_dict_list}

        mse_mae_dict = {(discovery_algorithm, measure, error): []
                        for discovery_algorithm in globals.algorithm_portfolio for error in ["mae", "mse"] for measure in globals.measure_portfolio}

        for i in range(no_cv):

            # to not use the same regresssors as before
            reset_all_cached_predictors()
            globals.regressors = {}
            # 0.8 training testing split
            ready_training, ready_testing = split_data(ready_logs)

            # clean data, remove rows with nan values
            ready_training = filter_instances_with_nan(ready_training)
            ready_testing = filter_instances_with_nan(ready_testing)

            init_regressors(ready_training, regression_method)

            # now we can for this iteration do multiple experiments with the same training/testing split

            # single_objective_min_max_accuracy_dict["token fitness"] = [avg1, avg2, avg3, avg4, avg5], where avg1 is the average accuracy for the first iteration

            # Experiment 1 compute regression_based classificatoin accuracy
            # own measure
            min_max_values = [evaluate_min_max_measure_accuracy(measure, ready_testing, regression_method)
                              for measure in globals.measure_portfolio]

            scikit_values = [evaluate_scikit_measure_accuracy(measure, ready_testing, f"regression_based_{regression_method}")
                             for measure in globals.measure_portfolio]

            for i in range(len(globals.measure_portfolio)):
                single_objective_min_max_accuracy_dict[globals.measure_portfolio[i]
                                                       ] += [min_max_values[i]]
                single_objective_scikit_accuracy_dict[globals.measure_portfolio[i]
                                                      ] += [scikit_values[i]]

            # Experiment 2 create scatter plots for every measure
            if not created_scatter_plot[regression_method]:
                for measure in globals.measure_portfolio:
                    create_scikit_regression_scatter_plot(
                        measure, regression_method, ready_testing, f"{regression_method}_{measure}")

            # Experiment 3 compute MSE/MAE values
            for discovery_algorithm in globals.algorithm_portfolio:
                for measure in globals.measure_portfolio:
                    mse, mae = mse_mae_computation(
                        ready_testing, regression_method, discovery_algorithm, measure)
                    mse_mae_dict[discovery_algorithm, measure, "mse"] += [mse]
                    mse_mae_dict[discovery_algorithm, measure, "mae"] += [mae]

            # Experiment 4 multiobjective accuracy
            # once with scikit accuracy
            # once with minmax normalization
            mo_min_max_values = [evaluate_mo_min_max_measure_accuracy(measure_weights_dict, ready_testing, regression_method)
                                 for measure_weights_dict in measure_weights_dict_list]
            mo_scikit_values = [evaluate_mo_scikit_measure_accuracy(measure_weights_dict, ready_testing, regression_method)
                                for measure_weights_dict in measure_weights_dict_list]
            for i in range(len(measure_weights_dict_list)):
                cur_measure_weights_dict = str(measure_weights_dict_list[i])
                multi_objective_min_max_accuracy_dict[cur_measure_weights_dict] += [
                    mo_min_max_values[i]]
                multi_objective_scikit_accuracy_dict[cur_measure_weights_dict] += [
                    mo_scikit_values[i]]
        # End of experiments now store results
        # Plot Experiment 1
        values = [np.mean(single_objective_min_max_accuracy_dict[measure])
                  for measure in globals.measure_portfolio]
        create_measure_bar_plot(
            globals.measure_portfolio, f"Accuracy {len(ready_testing)} CV {no_cv}", values, f"{regression_method}_min_max_accuracy")
        values = [np.mean(single_objective_scikit_accuracy_dict[measure])
                  for measure in globals.measure_portfolio]
        create_measure_bar_plot(
            globals.measure_portfolio, f"Accuracy {len(ready_testing)} CV {no_cv}", values, f"{regression_method}_scikit_accuracy")

        current_date = datetime.now()
        formatted_date = current_date.strftime('%Y_%m_%d')
        # Experiment 3 take averages over mses and maes
        for discovery_algorithm in globals.algorithm_portfolio:
            for measure in globals.measure_portfolio:

                storage_dir = f'../evaluation/{formatted_date}/mse_mae'
                os.makedirs(storage_dir, exist_ok=True)

                with open(f'{storage_dir}/{regression_method}.txt', 'a') as file:
                    # Loop through your algorithms and measures
                    for discovery_algorithm in globals.algorithm_portfolio:
                        for measure in globals.measure_portfolio:
                            # Assuming 'mae' is calculated or retrieved previously in your code

                            cur_avg_mse = np.mean(
                                mse_mae_dict[discovery_algorithm, measure, "mse"])
                            cur_avg_mae = np.mean(
                                mse_mae_dict[discovery_algorithm, measure, "mae"])
                            # Write the combination and its MAE to the file
                            file.write(
                                f"{discovery_algorithm} {measure} mse:{mse}\n")
                            file.write(
                                f"{discovery_algorithm} {measure} mae:{mse}\n")
        # Experiment 4
        string_encodings_of_measure_weights = [
            f"MW{i}" for i in range(len(measure_weights_dict_list))]
        values = [np.mean(multi_objective_min_max_accuracy_dict[str(measure_weights_dict)])
                  for measure_weights_dict in measure_weights_dict_list]
        create_measure_bar_plot(
            string_encodings_of_measure_weights, f"Accuracy {len(ready_testing)} CV {no_cv}", values, f"mo_{regression_method}_min_max_accuracy")

        values = [np.mean(multi_objective_scikit_accuracy_dict[str(measure_weights_dict)])
                  for measure_weights_dict in measure_weights_dict_list]
        create_measure_bar_plot(
            string_encodings_of_measure_weights, f"Accuracy {len(ready_testing)} CV {no_cv}", values, f"mo_{regression_method}_scikit_accuracy")
