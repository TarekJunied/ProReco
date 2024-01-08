from utils import read_model, read_log, load_cache_variable, store_cache_variable, generate_log_id, generate_cache_file,  read_log
import logging
import math
import numpy as np
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from tqdm.contrib.concurrent import process_map  # Use process_map from tqdm
from feature_controller import read_feature_matrix, read_feature_vector, get_total_feature_functions_dict, read_single_feature
from measures import read_target_entries, read_target_entry, read_classification_target_vector, read_measure_entry
from filehelper import gather_all_xes, split_file_path, get_all_ready_logs
from LogGenerator.log_generator import create_random_log
import multiprocessing
import globals
import random
import sys
import pm4py
import os


def fix_corrupt_cache():
    cache_folder = f"{globals.flask_app_path}/cache/"
    for folder_path, _, filenames in os.walk(cache_folder):
        for filename in filenames:
            if filename.endswith(".pkl"):
                file_path = os.path.join(folder_path, filename)

                try:
                    load_cache_variable(file_path)
                except Exception as e:
                    os.remove(file_path)
                    print(f"Error loading {file_path}: {e}")


def load_logs_into_main_memory(log_paths):
    for log_path in log_paths:
        globals.log_paths[log_path] = read_log(log_path)


def load_logs_into_main_memory_with_mode(log_paths, mode):
    if mode == "training":
        for log_path in log_paths:
            globals.training_log_pathslog_paths[log_path] = read_log(log_path)
    elif mode == "testing":
        for log_path in log_paths:
            globals.testing_log_paths[log_path] = read_log(log_path)
    else:
        print("wrong mode")


def load_models_into_main_memory(log_paths, algorithm_portfolio):
    for log_path in log_paths:
        for discovery_algorithm in algorithm_portfolio:
            globals.models[log_path, discovery_algorithm] = read_model(
                log_path, discovery_algorithm)


def load_features_into_main_memory(log_paths, selected_features):
    for log_path in log_paths:
        for feature in selected_features:
            globals.features[log_path, feature] = read_single_feature(
                log_path, feature)


def load_measures_into_main_main_memory(log_paths, algorithm_portfolio, selected_measures):
    for log_path in log_paths:
        for discovery_algorithm in algorithm_portfolio:
            for measure in selected_measures:
                globals.measures[log_path, discovery_algorithm,
                                 measure] = read_measure_entry(log_path, discovery_algorithm, measure)


def get_log_name(log_path):
    return split_file_path(log_path)["filename"]

# TODO: change util functions to try to read


def load_logs():
    training_log_paths = get_all_ready_logs_multiple(
        gather_all_xes("../logs/training"))
    testing_log_paths = get_all_ready_logs_multiple(
        gather_all_xes("../logs/testing"))

    load_logs_into_main_memory(training_log_paths + testing_log_paths)
    load_logs_into_main_memory_with_mode(training_log_paths, "training")
    load_logs_into_main_memory_with_mode(training_log_paths, "testing")


def load_measures():
    log_paths = list(globals.training_log_paths.keys()) + \
        list(globals.testing_log_paths.keys())

    load_measures_into_main_main_memory(
        log_paths, globals.algorithm_portfolio, globals.measure_portfolio)


def load_models():
    log_paths = list(globals.training_log_paths.keys()) + \
        list(globals.testing_log_paths.keys())
    load_models_into_main_memory(log_paths, globals.algorithm_portfolio)


def load_features():
    log_paths = list(globals.training_log_paths.keys()) + \
        list(globals.testing_log_paths.keys())
    load_features_into_main_memory(log_paths, globals.feature_portfolio)


def init_given_parameters(log_paths, algorithm_portfolio, selected_features, selected_measures):
    load_logs_into_main_memory(log_paths)
    load_features_into_main_memory(log_paths, selected_features)
    load_models_into_main_memory(log_paths, algorithm_portfolio)
    load_measures_into_main_main_memory(
        log_paths, algorithm_portfolio, selected_measures)


def init():
    load_logs()
    load_measures()
    load_models()
    load_features()


def init_log(log_path, feature_portfolio, algorithm_portfolio, measure_portfolio):

    read_log(log_path)
    for discovery_algorithm in algorithm_portfolio:
        read_model(log_path, discovery_algorithm)

    read_feature_vector(log_path, feature_portfolio)

    for measure in measure_portfolio:
        for discovery_algorithm in algorithm_portfolio:
            read_measure_entry(log_path, discovery_algorithm, measure)


def get_file_size(file_path):
    return os.path.getsize(file_path)


def sort_files_by_size(file_paths):
    return sorted(file_paths, key=get_file_size)


def try_init_log(log_path):
    list_of_measure_names = globals.measures
    try:
        read_log(log_path)
    except Exception as e:
        print("Could not parse log")
        print(e)

    try:
        read_feature_vector(log_path, globals.feature_portfolio)
    except Exception as e:
        print("Couldn't compute feature vector")
        print(e)

    for discovery_algorithm in globals.algorithm_portfolio:
        try:
            read_model(log_path, discovery_algorithm)
        except Exception as e:
            print(
                f"Could not discover model for {discovery_algorithm} on {log_path}")
            print(e)

    for measure in globals.measure_portfolio:
        for discovery_algorithm in globals.algorithm_portfolio:
            try:
                read_measure_entry(log_path, discovery_algorithm, measure)
            except Exception as e:
                print(
                    f"Could not compute measure {measure} on {discovery_algorithm}, {log_path}")
                print(e)


def reset_all_cached_predictors():
    paths = [f"./cache/regressors", f"./cache/explainers",
             f"./cache/optimal_features_lists"]
    for path in paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file != '.gitkeep':
                    os.remove(os.path.join(root, file))
    globals.regressors = {}
    print("cleared regressors from cacehe and main memory")


def filter_instances_with_nan(log_paths):
    no_list = []
    for log_path in log_paths:
        for feature in globals.feature_portfolio:
            val = read_single_feature(log_path, feature)
            if val is None or math.isnan(val) or np.isnan(val):
                no_list += [log_path]

    return [lp for lp in log_paths if lp not in no_list]


def clean_nan_features(all_ready_logs):
    evil_features = set()
    evil_logs = set()
    for log_path in all_ready_logs:
        for feature in globals.feature_portfolio:
            val = read_single_feature(log_path, feature)
            if val is None or math.isnan(val) or np.isnan(val):
                evil_features.add(feature)
                evil_logs.add(get_log_name(log_path))
                yesno = input(
                    f"do you want to delete the feature {feature} of {get_log_name(log_path)}")
                if yesno == "y":
                    os.remove(
                        f"./cache/features/{globals.flask_app_path}/cache/features/{feature}_{get_log_name(log_path)}.pkl")
    print("evil logs: ")
    print(evil_logs)
    print("evil features")
    print(evil_features)


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    reset_all_cached_predictors()
    all_logs = gather_all_xes("../logs")
    all_ready_logs = get_all_ready_logs(
        all_logs, globals.feature_portfolio, globals.algorithm_portfolio, globals.measure_portfolio)
    input(len(all_ready_logs))
    clean_nan_features(all_ready_logs)
    globals.feature_portfolio = list(get_total_feature_functions_dict().keys())
