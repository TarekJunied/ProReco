import subprocess
import pm4py
import time
import pickle
import os
import random
import hashlib
import globals
import math
from filehelper import  gather_all_xes
from discovery.splitminer.split_miner import discover_petri_net_split
from discovery.structuredminer.fodina_miner import discover_petri_net_fodina
from pm4py.algo.discovery.inductive import algorithm as inductive_miner


def get_log_name(log_path):
    return split_file_path(log_path)["filename"]


def split_file_path(file_path):
    # Split the file path into directory, filename, and extension
    directory, file_name_with_extension = os.path.split(file_path)
    file_name, file_extension = os.path.splitext(file_name_with_extension)

    return {
        'directory': directory,
        'filename': file_name,
        'extension': file_extension
    }


def generate_log_id(log_path):
    return split_file_path(log_path)["filename"]


def print_distinct_traces(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list(variants.keys())

    for trace in trace_variants:
        print(trace)


def compute_model(log_path, discovery_algorithm):
    log = read_log(log_path)

    print(f"Start compute_model using {discovery_algorithm}")
    
    return discovery_functions[discovery_algorithm](log)





def read_model(log_path, discovery_algorithm):


    if (log_path,discovery_algorithm) in globals.models:
        return model


    log_id = generate_log_id(log_path)
    cache_file_path = generate_cache_file(
        f"./cache/models/{discovery_algorithm}_{log_id}.pkl")
    runtime_cache_file_path = generate_cache_file(
        f"./cache/measures/{discovery_algorithm}_runtime_{log_id}.pkl")
    log_runtime_cache_file_path = generate_cache_file(
        f"./cache/measures/{discovery_algorithm}_log_runtime_{log_id}.pkl")
    try:
            model = load_cache_variable(cache_file_path)
            runtime = load_cache_variable(runtime_cache_file_path)
            log_runtime = load_cache_variable(runtime_cache_file_path)
    except Exception:
        print(
                f"No cached model found, now computing model for {log_path} using {discovery_algorithm}.")

        start_time = time.time()
        model = compute_model(log_path, discovery_algorithm)
        end_time = time.time()

        store_cache_variable(
            end_time-start_time, runtime_cache_file_path)
        store_cache_variable(model, cache_file_path)
        store_cache_variable(math.log10(end_time - start_time), log_runtime_cache_file_path)
    return model


def store_cache_variable(variable_to_cache, cache_file_path):
    try:
        with open(cache_file_path, 'wb') as cache_file:
            pickle.dump(variable_to_cache, cache_file)
        print(f"Variable stored in cache file: {cache_file_path}")
    except Exception as e:
        print(f"Error storing variable in cache: {str(e)}")


def load_cache_variable(cache_file_path):
    with open(cache_file_path, 'rb') as cache_file:
        loaded_variable = pickle.load(cache_file)
    print(f"Variable loaded from cache file: {cache_file_path}")
    return loaded_variable


def generate_cache_file(cache_filepath):
    if not os.path.exists(cache_filepath):
        print("Cache file does not exist yet.")
        with open(cache_filepath, 'w') as file:
            pass
        print(f"File '{cache_filepath}' created.")
    return cache_filepath


def read_log(log_path):
    if log_path in globals.training_log_paths:
            return globals.training_log_paths[log_path]
    elif log_path in globals.testing_log_paths:
            return globals.testing_log_paths[log_path]
    
    log_id = generate_log_id(log_path)
    cache_file_path = generate_cache_file(f"./cache/logs/{log_id}.pkl")
    log = None
    try:
            log = load_cache_variable(cache_file_path)
    except Exception:
        print("No cached log found, now parsing log.")
        log = pm4py.read.read_xes(log_path)
        store_cache_variable(log, cache_file_path)
    return log


def read_logs(log_paths):
    for log_path in log_paths:
        read_log(log_path)


def read_models(log_paths):
    for log_path in log_paths:
        for discovery_algorithm in globals.algorithm_portfolio:
            read_model(log_path, discovery_algorithm)


def all_files_exist(file_paths):
    """
    Check if all files in the given list exist.

    Parameters:
    - file_paths (list): List of file paths to check.

    Returns:
    - bool: True if all files exist, False otherwise.
    """
    return all(os.path.exists(file_path) for file_path in file_paths)


    
def get_all_ready_logs(log_paths, measure_name):
    ready_logs = []
    for log_path in log_paths:
        file_list = []
        log_id = generate_log_id(log_path)
        log_cache = f"./cache/logs/{log_id}.pkl"
        features_cache = f"./cache/features/feature_{log_id}.pkl"
        file_list += [log_cache, features_cache]
        for discovery_algorithm in globals.algorithm_portfolio:
            model_path = f"./cache/models/{discovery_algorithm}_{log_id}.pkl"
            measure_cache = f"./cache/measures/{discovery_algorithm}_{measure_name}_{log_id}.pkl"
            file_list += [model_path, measure_cache]

        if all_files_exist(file_list):
            ready_logs += [log_path]

    return ready_logs


def split_data(data, ratio=0.8, seed=None):

    if seed is not None:
        random.seed(seed)

    # Shuffle the data to ensure randomness in the split
    random.shuffle(data)

    # Calculate the split index based on the ratio
    split_index = int(len(data) * ratio)

    # Split the data into training and testing sets
    training_data = data[:split_index]
    testing_data = data[split_index:]

    return training_data, testing_data

def discover_petri_net_inductive_infrequent(log):
    return inductive_miner.apply(
                log, variant=inductive_miner.Variants.IMf
    )

def discover_petri_net_inductive_direct(log): 
    return inductive_miner.apply(
                log, variant=inductive_miner.Variants.IMd
            )


discovery_functions = {
    "alpha":pm4py.discover_petri_net_alpha,
    "alpha_plus":pm4py.discover_petri_net_alpha_plus,
    "heuristic":pm4py.discover_petri_net_heuristics,
    "inductive":pm4py.discover_petri_net_ilp,
    "split":discover_petri_net_split,
    "inductive_infrequent":discover_petri_net_inductive_infrequent,
    "inductive_direct":discover_petri_net_inductive_direct
}

if __name__ == "__main__":
    log_paths = gather_all_xes("../logs/training")
    log = read_log(log_paths[1])
    for discovery_algorithm in globals.algorithm_portfolio:
        read_model(log_paths[1], discovery_algorithm)
        input(f"{discovery_algorithm} is done")