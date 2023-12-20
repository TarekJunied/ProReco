from utils import read_logs, read_models, read_model, read_log, load_cache_variable, store_cache_variable, generate_log_id, generate_cache_file,  read_log
import logging

from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from tqdm.contrib.concurrent import process_map  # Use process_map from tqdm
from feature_controller import read_feature_matrix, read_feature_vector, get_total_feature_functions_dict, read_single_feature
from measures import read_target_entries, read_target_entry, read_classification_target_vector, read_measure_entry
from filehelper import gather_all_xes, split_file_path
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
        log_paths, globals.algorithm_portfolio, globals.measures_list)


def load_models():
    log_paths = list(globals.training_log_paths.keys()) + \
        list(globals.testing_log_paths.keys())
    load_models_into_main_memory(log_paths, globals.algorithm_portfolio)


def load_features():
    log_paths = list(globals.training_log_paths.keys()) + \
        list(globals.testing_log_paths.keys())
    load_features_into_main_memory(log_paths, globals.selected_features)


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


def init_log(log_path, feature_portfolio, algorithm_portfolio):
    list_of_measure_names = globals.measures

    read_log(log_path)
    for discovery_algorithm in algorithm_portfolio:
        read_model(log_path, discovery_algorithm)

    read_feature_vector(log_path, feature_portfolio)

    for measure in list_of_measure_names:
        for discovery_algorithm in algorithm_portfolio:
            try:
                read_measure_entry(log_path, discovery_algorithm, measure)
            except Exception as e:
                print(e)


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
        read_feature_vector(log_path, globals.selected_features)
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

    for measure in list_of_measure_names:
        for discovery_algorithm in globals.algorithm_portfolio:
            try:
                read_measure_entry(log_path, discovery_algorithm, measure)
            except Exception as e:
                print(
                    f"Could not compute measure {measure} on {discovery_algorithm}, {log_path}")
                print(e)


if __name__ == "__main__":
    sys.setrecursionlimit(100000)

    log_folder_paths = []

    # Check if at least one argument is provided
    if len(sys.argv) > 1:
        # sys.argv[1] is the first command line argument
        for i in range(1, len(sys.argv)):
            log_folder_paths += [sys.argv[i]]
    else:
        print("No input provided")
        sys.exit(-1)

    globals.algorithm_portfolio = ["alpha", "alpha_plus", "inductive",
                                   "inductive_infrequent", "inductive_direct", "heuristic"]
    # , "ILP"

    globals.selected_features = list(get_total_feature_functions_dict().keys())

    logs_to_init = []
    for log_folder_path in log_folder_paths:
        logs_to_init += gather_all_xes(log_folder_path)
    # logs_to_init = sort_files_by_size(logs_to_init)

    num_processes = 20
    # sys.stdout = open('/dev/null', 'w')

    # process_map(try_init_log, logs_to_init, max_workers=num_processes)

    pool = multiprocessing.Pool(processes=num_processes)

    print("now mapping pool")
    pool.map(try_init_log, logs_to_init)

    print("pool map done")
    pool.close()
    print("pool closed")
    pool.join()
    print("pool joined")

    print("done")

    for log_path in logs_to_init:
        try:
            read_model(log_path, "ILP")
            read_model(log_path, "split")
        except Exception:
            print("bye next")
