
import os
import time
import subprocess
from filehelper import gather_all_xes
from utils import read_model, read_log, load_cache_variable, store_cache_variable, generate_log_id, generate_cache_file,  read_log
import logging
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


def all_init(log_path):
    for feature in globals.selected_features:
        try:
            read_single_feature(log_path, feature)
        except Exception as e:
            print(e)
            print(f"computation of {feature} on {log_path} failed")

    for discovery_algorithm in globals.algorithm_portfolio:
        try:
            read_model(log_path, discovery_algorithm)
        except Exception as e:
            print(f"mining using {discovery_algorithm} on {log_path} failed")
        # Your existing code for algorithm initialization
        for measure_name in globals.measures_list:
            try:
                log_id = generate_log_id(log_path)
                model_exists = load_cache_variable(
                    f"./cache/models/{discovery_algorithm}_{log_id}.pkl")
            except Exception as e:
                print(
                    "No process model exists for this log discovery algorithm combination")
                print("now exiting")
                return
            try:
                read_measure_entry(log_path, discovery_algorithm, measure_name)
            except Exception as e:
                print(e)
                print(
                    f"computing of {measure_name} on the model discovered by {discovery_algorithm} on event log {log_path} failed !")

    print("sucess !")


if __name__ == "__main__":
    globals.selected_features = list(get_total_feature_functions_dict().keys())
    log_path = sys.argv[1]

    all_init(log_path)
