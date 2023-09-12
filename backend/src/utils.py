import subprocess
import pm4py
import time
import pickle
import os
import random
import globals
from filehelper import *
from discovery.splitminer.split_miner import discover_petri_net_split
from discovery.structuredminer.fodina_miner import discover_petri_net_fodina


def generate_log_id(log_path):
    return get_file_name(log_path)

def print_distinct_traces(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list(variants.keys())

    for trace in trace_variants:
        print(trace)


def compute_model(log_path, discovery_algorithm):
    log = read_log(log_path)
    print(f"Start compute_model using {discovery_algorithm}")
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
        net, initial_marking, final_marking = discover_petri_net_split(
            log_path)

    elif discovery_algorithm == "fodina":
        net, initial_marking, final_marking = discover_petri_net_fodina(
            log_path)

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
            f"./cache/measures/{discovery_algorithm}_runtime_{log_id}")
        store_cache_variable(
        end_time-start_time, f"./cache/measures/{discovery_algorithm}_runtime_{log_id}")
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
    if not os.path.exists(cache_filepath):
        print("Cache file does not exist.")
        with open(cache_filepath, 'w') as file:
            pass
        print(f"File '{cache_filepath}' created.")
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


def read_logs(log_paths):

    for log_path in log_paths:
        read_log(log_path)


def read_models(log_paths):
    for log_path in log_paths:
        for discovery_algorithm in globals.algorithm_portfolio:
            print(
                f"Now start discovery of {log_path} using {discovery_algorithm}")
            try:
                read_model(log_path, discovery_algorithm)
            except Exception as e:
                print(
                    f"Could not discover {log_path} using {discovery_algorithm}, because: ")
                print("An error occurred:", e)



def split_list(input_list, n):
    # Calculate the length of each sublist
    sublist_length = len(input_list) // n
    remainder = len(input_list) % n  # Calculate the remainder

    # Initialize the list of sublists
    sublists = []

    # Split the input_list into sublists
    start = 0
    for i in range(n):
        if i < remainder:
            end = start + sublist_length + 1
        else:
            end = start + sublist_length

        sublist = input_list[start:end]
        sublists.append(sublist)
        start = end

    return sublists





def split_data(data, ratio=0.8, seed=None):
    """
    Splits a list of data into training and testing sets based on the given ratio.

    Parameters:
    - data: The list of instances to be split.
    - ratio: The ratio of data to be included in the training set (default is 0.8).
    - seed: Random seed for reproducibility (optional).

    Returns:
    - A tuple containing two lists: (training_data, testing_data).
    """
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



#TODO : can be deleted later once, naming convention is clear
def fix_pkl_names(log_paths):

    for log_path in log_paths:

        log_id = generate_log_id(log_path)

        if contains_space(log_path):
            input("stop now")
       
        cur_pkls = find_files_with_substring("./cache",log_id)

        file_name = get_file_name(log_path)

        for cur_file in cur_pkls:
            replace_substring_and_rename_file(cur_file, log_id,file_name)








if __name__ == "__main__":
    log_paths = gather_all_xes("../logs/logs_in_xes") + gather_all_xes("./LogGenerator/logs")


    

        

    
