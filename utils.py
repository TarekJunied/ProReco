import importlib

import pm4py
import time
import pickle
from globals import algorithm_portfolio, pickled_variables, models, training_logs_paths, feature_vectors, logs, target_vectors, runtime, X, y, cache_file


def print_distinct_traces(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list(variants.keys())

    for trace in trace_variants:
        print(trace)


def read_model(log_path, discovery_algorithm):
    if (log_path, discovery_algorithm) not in models:
        log = read_log(log_path)
        start_time = time.time()
        if discovery_algorithm == "alpha":
            net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(
                log)
            models[log_path, discovery_algorithm] = (
                net, initial_marking, final_marking)

        elif discovery_algorithm == "heuristic":
            net, initial_marking, final_marking = pm4py.discover_petri_net_heuristics(
                log)
            models[log_path, discovery_algorithm] = (
                net, initial_marking, final_marking)
        elif discovery_algorithm == "ILP":
            net, initial_marking, final_marking = pm4py.discover_petri_net_ilp(
                log)
            models[log_path, discovery_algorithm] = (
                net, initial_marking, final_marking)

        elif discovery_algorithm == "inductive":
            net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(
                log)
            models[log_path, discovery_algorithm] = (
                net, initial_marking, final_marking)
        end_time = time.time()

        runtime[log_path, discovery_algorithm] = end_time - start_time

    return models[log_path, discovery_algorithm]


def read_log(log_path):
    if log_path in logs:
        return logs[log_path]
    else:
        try:
            log = pm4py.read_xes(log_path)
            logs[log_path] = log
            return log
        except Exception:
            print("The log does not exist !")


def read_logs():
    global training_logs_paths
    input(training_logs_paths)
    for log_path in training_logs_paths:
        try:
            log = pm4py.read_xes(log_path)
            logs[log_path] = log
        except Exception:
            print("The log does not exist!")

    pickled_variables["training_logs_paths"] = training_logs_paths
    pickled_variables["logs"] = logs


def compute_models():
    for log_path in training_logs_paths:
        for discovery_algorithm in algorithm_portfolio:
            read_model(log_path, discovery_algorithm)

    pickled_variables["runtime"] = runtime
    pickled_variables["models"] = models


def pickle_dump():
    global pickled_variables

    with open(cache_file, "wb") as f:
        pickle.dump(pickled_variables, f)
        print("Data cached.")


def pickle_retrieve():
    global pickled_variables
    try:
        with open(cache_file, "rb") as f:
            pickled_variables = pickle.load(f)
        print("Cached data loaded.")
    except FileNotFoundError:
        pickled_variables = None
        print("No pickle file found")


def load_all_globals_from_cache():
    global pickled_variables, models, training_logs_paths, feature_vectors, logs, target_vectors, runtime, X, y
    models = pickled_variables["models"]
    training_logs_paths = pickled_variables["training_log_paths"]
    feature_vectors = pickled_variables["logs"]
    logs = pickled_variables["logs"]
    target_vectors = pickled_variables["target_vectors"]
    runtime = pickled_variables["runtime"]
