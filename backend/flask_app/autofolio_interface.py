import csv
import globals
import numpy as np
import sys
import os
import subprocess
import re
from feature_controller import read_single_feature
from utils import get_log_name
from filehelper import gather_all_xes, get_all_ready_logs_multiple
from measures import read_measure_entry


def create_csv_from_list(data, filepath):
    """
    data = [
    ['Name', 'Age', 'City'],
    ['John Doe', 25, 'New York'],
    ['Jane Smith', 30, 'San Francisco'],
    ['Bob Johnson', 22, 'Los Angeles']
    ]
    Args:
        look at above
    """
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(data[0])

        # Write the remaining rows
        writer.writerows(data[1:])

        print(f'CSV file "{filepath}" has been created.')


def create_feature_csv(log_paths, filepath):
    first_row = [""] + globals.selected_features
    data = [first_row]
    i = 1
    for log_path in log_paths:
        cur_row = [f"inst{i}"]
        for feature in globals.selected_features:
            cur_row += [read_single_feature(log_path, feature)]
        data += [cur_row]
        i += 1

    create_csv_from_list(data, filepath)


def create_performance_csv(log_paths, measure_name, filepath):
    first_row = [""] + globals.algorithm_portfolio
    data = [first_row]
    i = 1
    for log_path in log_paths:
        cur_row = [f"inst{i}"]
        for discovery_algorithm in globals.algorithm_portfolio:
            cur_row += [read_measure_entry(log_path,
                                           discovery_algorithm, measure_name)]
        data += [cur_row]
        i += 1

    create_csv_from_list(data, filepath)


def create_autofolio_predictor(training_logpaths, measure_name):

    training_features_filename = f"{measure_name}_training_features.csv"
    training_performance_filename = f"{measure_name}_training_performance.csv"

    training_features_filepath = f"./AutoFolio/csv_files/{measure_name}_training_features.csv"
    training_performance_filepath = f"./AutoFolio/csv_files/{measure_name}_training_performance.csv"
    testing_features_filepath = f"./AutoFolio/csv_files/{measure_name}_testing_features.csv"
    testing_performance_filepath = f"./AutoFolio/csv_files/{measure_name}_testing_performance.csv"

    create_feature_csv(training_logpaths, training_features_filepath)
    create_performance_csv(training_logpaths, measure_name,
                           training_performance_filepath)

    # create_feature_csv(testing_logpaths,testing_features_filepath)
    # create_performance_csv(testing_logpaths,measure_name,testing_performance_filepath)

    predictor_filepath = f"./af_predictors/{measure_name}_predictor.af"

    if globals.measures_kind[measure_name] == "max":
        max_string = "--maximize"
    elif globals.measures_kind[measure_name] == "min":
        max_string = ""
    else:
        print("invalid kind of measure")
        sys.exit(-1)

    if measure_name == "runtime" or measure_name == "log_runtime":
        objective_string = "runtime"
    else:
        objective_string = "solution_quality"
    objective_string = "solution_quality"

    command = [
        "python",
        f"./scripts/autofolio",
        "--performance_csv", f"./csv_files/{training_performance_filename}",
        "--feature_csv",  f"./csv_files/{training_features_filename}",
        "--objective ", objective_string,
        "--tune",
        max_string,
        "--save", predictor_filepath,

    ]

    command_str = " ".join(command)

    os.chdir(os.path.abspath("./AutoFolio"))

    subprocess.run(command_str, shell=True)

    os.chdir("../")
    return predictor_filepath


def extract_prediction_from_autofolio_string(autofolio_string):
    # Define a regular expression pattern to capture the word after "('inductive',"
    pattern = r"\('(\w+)',"

    # Use re.search to find the first match
    match = re.search(pattern, autofolio_string)

    # Check if a match is found
    if match:
        # Extract and return the captured word
        return match.group(1)
    else:
        # Return None if no match is found
        return "AutoFolio Error"


def read_autofolio_predictor(training_logpaths, measure_name):
    if os.path.exists(f"./AutoFolio/af_predictors/{measure_name}_predictor.af"):
        ret = f"./af_predictors/{measure_name}_predictor.af"
    else:
        ret = f"{create_autofolio_predictor(training_logpaths,measure_name)}"
    return ret


def autofolio_classification(log_path, ready_training, measure_name):

    predictor_filepath = read_autofolio_predictor(ready_training, measure_name)

    spaced_out_feature_vector_string = space_out_feature_vector_string(
        log_path)

    command = [
        "python",
        "scripts/autofolio",
        "--load",
        predictor_filepath,
        "--feature_vec",
        spaced_out_feature_vector_string]

    os.chdir("./AutoFolio")

    try:
        output = subprocess.check_output(
            command, stderr=subprocess.STDOUT, text=True)
        print("Command output:")
        print(output)
    except subprocess.CalledProcessError as e:
        print("Error executing command. Return code:", e.returncode)
        print("Command output (if any):")
        print(e.output)

    prediction = extract_prediction_from_autofolio_string(output)

    if prediction not in globals.algorithm_portfolio:
        return

    os.chdir("../")

    return prediction


if __name__ == "__main__":
    ready_training = get_all_ready_logs_multiple(
        gather_all_xes("../logs/training"))
    for measure in globals.measures_list:
        create_autofolio_predictor(ready_training, measure)
