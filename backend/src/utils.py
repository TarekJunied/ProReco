import subprocess
import pm4py
import time
import pickle
import os
import uuid
import datetime
import globals
import hashlib
from filehelper import gather_all_xes
from discovery.splitminer.split_miner import discover_petri_net_split
from discovery.structuredminer.fodina_miner import discover_petri_net_fodina


def generate_log_id(log_path):
    sha256 = hashlib.sha256()
    sha256.update(log_path.encode('utf-8'))
    hash_hex = sha256.hexdigest()
    hash_bits = int(hash_hex[:32 // 4], 16)
    return str(hash_bits)


def print_distinct_traces(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list(variants.keys())

    for trace in trace_variants:
        print(trace)


def compute_model(log_path, discovery_algorithm):
    log = read_log(log_path)
    if discovery_algorithm == "alpha":
        net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(
            log)
    elif discovery_algorithm == "heuristic":
        net, initial_marking, final_marking = pm4py.discover_petri_net_heuristics(
            log)
    elif discovery_algorithm == "ILP":
        net, initial_marking, final_marking = pm4py.discover_petri_net_ilp(
            log)
    elif discovery_algorithm == "inductive":
        net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(
            log)
    elif discovery_algorithm == "split":
        current_path = os.getcwd()
        net, initial_marking, final_marking = discover_petri_net_split(
            current_path + "/" + log_path)

    elif discovery_algorithm == "fodina":
        current_path = os.getcwd()
        net, initial_marking, final_marking = discover_petri_net_fodina(
            current_path + "/" + log_path)

    return net, initial_marking, final_marking


def read_model(log_path, discovery_algorithm):
    # TODO don't forget runtime
    log_id = generate_log_id(log_path)
    cache_file_path = generate_cache_file(
        f"./cache/models/{discovery_algorithm}_{log_id}.pkl")
    try:
        print(cache_file_path)
        model = load_cache_variable(cache_file_path)
    except Exception:
        print(
            f"No cached model found, now computing model for {log_path} using {discovery_algorithm}.")

        start_time = time.time()
        model = compute_model(log_path, discovery_algorithm)
        end_time = time.time()

        globals.models[log_path, discovery_algorithm] = model
        generate_cache_file(
            f"./cache/models/runtime/runtime_{discovery_algorithm}_{log_id}.pkl")
        store_cache_variable(
            end_time-start_time, f"./cache/measures/runtime/runtime_{discovery_algorithm}_{log_id}")
        store_cache_variable(model, cache_file_path)
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

    if not os.path.isfile(cache_filepath):
        try:
            # Attempt to create the file
            with open(cache_filepath, 'w') as new_file:
                pass
        except Exception as e:
            print(f"An error occurred: {e}")
    return cache_filepath


def read_log(log_path):
    log_id = generate_log_id(log_path)
    cache_file_path = generate_cache_file(f"./cache/logs/{log_id}.pkl")
    try:
        log = load_cache_variable(cache_file_path)
    except Exception:
        print("No cached log found, now parsing log.")
        log = pm4py.read.read_xes(log_path)
        globals.logs[log_path] = log
        store_cache_variable(log, cache_file_path)
    return log


def read_logs(logs_dir):
    log_paths = gather_all_xes(logs_dir)

    for log_path in log_paths:
        read_log(log_path)


def read_models(log_paths_dir):
    for log_path in log_paths_dir:
        for discovery_algorithm in globals.algorithm_portfolio:
            print(
                f"Now start discovery of {log_path} using {discovery_algorithm}")
            try:
                read_model(log_path, discovery_algorithm)
            except Exception:
                print(
                    f"Could not discover {log_path} using {discovery_algorithm} ")


def pickle_dump():

    with open(globals.cache_file, "wb") as f:
        pickle.dump(globals.pickled_variables, f)
        print("Data cached.")


def pickle_retrieve():
    with open(globals.cache_file, "rb") as f:
        try:
            globals.pickled_variables = pickle.load(f)
            print("Cached data loaded.")
        except Exception:
            globals.pickled_variables = {}
            print("Empty pickle. No pickled variables found.")


def load_all_globals_from_cache():
    globals.models = globals.pickled_variables["models"]
    globals.X = globals.pickled_variables["X"]
    globals.training_logs_paths = globals.pickled_variables["training_logs_paths"]
    globals.feature_vectors = globals.pickled_variables["logs"]
    globals.logs = globals.pickled_variables["logs"]
    globals.target_vectors = globals.pickled_variables["target_vectors"]
    globals.runtime = globals.pickled_variables["runtime"]


def load_target_vector_into_y():
    globals.y = [None] * len(globals.training_logs_paths)
    for i in range(len(globals.training_logs_paths)):
        globals.y[i] = globals.target_vectors[globals.training_logs_paths[i],
                                              globals.selected_measure]


log_paths = gather_all_xes("./LogGenerator/logs")
for log_path in log_paths:
    read_log(log_path)

for log_path in log_paths:
    read_model(log_path, "alpha")
