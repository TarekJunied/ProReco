

from utils import read_log, generate_log_id, generate_cache_file, store_cache_variable, load_cache_variable
from filehelper import gather_all_xes, get_all_ready_logs_multiple
from flask_app.features.mtl_features.mtl_feature_interface import get_mtl_feature_functions_dict
from flask_app.features.own_features import *
from flask_app.features.fig4pm_features.fig4pm_interface import get_fig4pm_feature_functions_dict
import sys
import pm4py
import time
import globals
import math
import warnings
import numpy as np
sys.path.insert(
    0, '/rwthfs/rz/cluster/home/qc261227/Recommender/RecommenderSystem/backend/flask_app')

warnings.filterwarnings("ignore")

sys.path.append(
    "/home/qc261227/Recommender/RecommenderSystem/backend/flask_app/features/fig4pm_features")
sys.path.append(
    "/home/qc261227/Recommender/RecommenderSystem/backend/flask_app/features/fig4pm_features/measures_extracted_from_literature")


def compute_feature_vector(log_path):
    feature_vector = np.empty((1, len(globals.selected_features)))
    for feature_index in range(len(globals.selected_features)):
        feature_vector[0, feature_index] = compute_feature_log_path(
            log_path, feature_index)
    return feature_vector


def read_single_feature(log_path, feature_name):
    if (log_path, feature_name) in globals.features:
        return globals.features[log_path, feature_name]
    try:
        log_id = generate_log_id(log_path)
        cache_file_path = generate_cache_file(
            f"{globals.flask_app_path}/cache/features/{feature_name}_{log_id}.pkl")
        feature = load_cache_variable(cache_file_path)
    except Exception:

        print("feature not cached,  now computing single feature")
        feature = compute_feature_log_path(
            log_path, globals.selected_features.index(feature_name))
        store_cache_variable(feature, cache_file_path)
    return feature


def read_feature_vector(log_path):
    feature_vector = np.empty((1, len(globals.selected_features)))
    for feature_index in range(len(globals.selected_features)):
        feature_vector[0, feature_index] = read_single_feature(
            log_path, globals.selected_features[feature_index])
    return feature_vector


def read_feature_matrix(log_paths):
    x = np.empty((len(log_paths),
                  len(globals.selected_features)))
    for log_index in range(len(log_paths)):
        x[log_index, :] = read_feature_vector(log_paths[log_index])
    return x


def read_subset_features(log_paths):
    for log_index in range(len(log_paths)):
        globals.X[log_index, :] = read_feature_vector(log_paths[log_index])


def compute_feature_log_path(log_path, feature_index):
    feature_name = globals.selected_features[feature_index]

    # Check if the feature name is valid
    if feature_name in feature_functions:
        # Call the corresponding feature function
        ret = feature_functions[feature_name](log_path)
        return ret
    else:

        print("Invalid feature name")
        print(feature_name)
        input(feature_name)
        return None


def compute_feature(log_index, feature_index):
    log_path = globals.training_logs_paths[log_index]
    return compute_feature_log_path(log_path, feature_index)


def space_out_feature_vector_string(log_path):
    feature_vector = read_feature_vector(log_path)
    spaced_out_vector = ""
    for feature_index in range(len(globals.selected_features)-1):
        spaced_out_vector = spaced_out_vector + \
            str(feature_vector[0, feature_index]) + " "
    spaced_out_vector += str(feature_vector[0,
                             len(globals.selected_features)-1])
    return spaced_out_vector


#    "density": feature_density,
feature_functions = {
    "no_distinct_traces": feature_no_distinct_traces,
    "no_total_traces": feature_no_total_traces,
    "avg_trace_length": feature_avg_trace_length,
    "avg_event_repetition_intra_trace": feature_avg_event_repetition_intra_trace,
    "no_distinct_events": feature_no_distinct_events,
    "no_events_total": feature_no_events_total,
    "no_distinct_start": feature_no_distinct_start,
    "no_distinct_end": feature_no_distinct_end,
    "length_one_loops": feature_length_one_loops,
    "total_no_activities": feature_total_no_activities,
    "percentage_concurrency": feature_percentage_concurrency,
    "percentage_sequence": feature_percentage_sequence,
    "dfg_mean_variable_degree": feature_dfg_mean_variable_degree,
    "dfg_variation_coefficient_variable_degree": feature_dfg_variation_coefficient_variable_degree,
    "dfg_min_variable_degree": feature_dfg_min_variable_degree,
    "dfg_max_variable_degree": feature_dfg_max_variable_degree,
    "dfg_entropy_variable_degree": feature_dfg_entropy_variable_degree,
    "dfg_wcc_variation_coefficient": feature_dfg_wcc_variation_coefficient,
    "dfg_wcc_min": feature_dfg_wcc_min,
    "dfg_wcc_max": feature_dfg_wcc_max,
    "dfg_wcc_entropy": feature_dfg_wcc_entropy,

}

if __name__ == "__main__":

    mtl_dict = get_mtl_feature_functions_dict()
    fig4pm_dict = get_fig4pm_feature_functions_dict()
    feature_functions = {**mtl_dict, **fig4pm_dict, **feature_functions}
    globals.algorithm_portfolio = ["alpha", "inductive"]
    log_paths = get_all_ready_logs_multiple(gather_all_xes("../logs/training"))
    globals.selected_features = list(feature_functions.keys())
    for log_path in log_paths:
        failed_features = []
        for feature_name in feature_functions:
            read_single_feature(log_path, feature_name)
