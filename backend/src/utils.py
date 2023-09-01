import subprocess
import pm4py
import time
import pickle
import os
import globals
from discovery.splitminer.split_miner import discover_petri_net_split
from discovery.structuredminer.fodina_miner import discover_petri_net_fodina


def print_distinct_traces(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list(variants.keys())

    for trace in trace_variants:
        print(trace)


def read_model(log_path, discovery_algorithm):
    if (log_path, discovery_algorithm) not in globals.models:
        log = read_log(log_path)
        start_time = time.time()
        if discovery_algorithm == "alpha":
            net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(
                log)
            globals.models[log_path, discovery_algorithm] = (
                net, initial_marking, final_marking)

        elif discovery_algorithm == "heuristic":
            net, initial_marking, final_marking = pm4py.discover_petri_net_heuristics(
                log)
            globals.models[log_path, discovery_algorithm] = (
                net, initial_marking, final_marking)
        elif discovery_algorithm == "ILP":
            net, initial_marking, final_marking = pm4py.discover_petri_net_ilp(
                log)
            globals.models[log_path, discovery_algorithm] = (
                net, initial_marking, final_marking)

        elif discovery_algorithm == "inductive":
            net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(
                log)
            globals.models[log_path, discovery_algorithm] = (
                net, initial_marking, final_marking)

        elif discovery_algorithm == "split":
            current_path = os.getcwd()
            net, initial_marking, final_marking = discover_petri_net_split(
                current_path+ "/" + log_path)
            globals.models[log_path, discovery_algorithm] = (
                net, initial_marking, final_marking)
        elif discovery_algorithm == "fodina":
            current_path = os.getcwd()
            net, initial_marking, final_marking = discover_petri_net_fodina(
                current_path+ "/" + log_path)
            globals.models[log_path, discovery_algorithm] = (
                net, initial_marking, final_marking)
        end_time = time.time()

        globals.runtime[log_path, discovery_algorithm] = end_time - start_time

    return globals.models[log_path, discovery_algorithm]


def read_log(log_path):
    if log_path in globals.logs:
        return globals.logs[log_path]
    else:
        try:
            log = pm4py.read_xes(log_path)
            globals.logs[log_path] = log
            return log
        except Exception:
            print("The log does not exist !")


def read_logs():
    for log_path in globals.training_logs_paths:
        try:
            log = pm4py.read_xes(log_path)
            globals.logs[log_path] = log
        except Exception:
            print("The log does not exist!")

    globals.pickled_variables["training_logs_paths"] = globals.training_logs_paths
    globals.pickled_variables["logs"] = globals.logs


def compute_models():
    for log_path in globals.training_logs_paths:
        for discovery_algorithm in globals.algorithm_portfolio:
            read_model(log_path, discovery_algorithm)
            print(
                f"model by {discovery_algorithm} for {log_path} has been discovered")
    globals.pickled_variables["runtime"] = globals.runtime
    globals.pickled_variables["models"] = globals.models


def pickle_dump():

    with open(globals.cache_file, "wb") as f:
        pickle.dump(globals.pickled_variables, f)
        print("Data cached.")


def pickle_retrieve():
    try:
        with open(globals.cache_file, "rb") as f:
            globals.pickled_variables = pickle.load(f)
        print("Cached data loaded.")
    except FileNotFoundError:
        globals.pickled_variables = None
        print("No pickle file found")


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
