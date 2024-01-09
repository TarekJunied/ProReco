import os
import numpy as np
import warnings
import math
import globals
import time
import pm4py
import sys
from flask_app.utils import read_log, generate_log_id, generate_cache_file, store_cache_variable, load_cache_variable, get_log_name
from flask_app.features.removed_features import get_removed_features_list
from flask_app.features.fig4pm_features.fig4pm_interface import get_fig4pm_feature_functions_dict
from flask_app.features.own_features import get_own_features_dict
from flask_app.features.mtl_features.mtl_feature_interface import get_mtl_feature_functions_dict
from flask_app.filehelper import gather_all_xes, get_all_ready_logs


warnings.filterwarnings("ignore")


def read_single_feature(log_path, feature_name):
    log_name = get_log_name(log_path)
    if (log_path, feature_name) in globals.features:
        return globals.features[log_path, feature_name]
    try:

        log_id = generate_log_id(log_path)
        cache_file_path = generate_cache_file(
            f"{globals.flask_app_path}/cache/features/{feature_name}_{log_id}.pkl")
        feature = load_cache_variable(cache_file_path)
    except Exception:

        print("feature not cached,  now computing single feature")
        feature = compute_single_feature(log_path, feature_name)
        store_cache_variable(feature, cache_file_path)
    return feature


def read_feature_vector(log_path, feature_portfolio):
    feature_vector = np.empty((1, len(feature_portfolio)))
    i = 0
    for feature in feature_portfolio:
        feature_vector[0, i] = read_single_feature(
            log_path, feature)
        i += 1
    return feature_vector


def read_feature_matrix(log_paths, feature_portfolio):
    x = np.empty((len(log_paths),
                  len(feature_portfolio)))
    for log_index in range(len(log_paths)):
        x[log_index, :] = read_feature_vector(
            log_paths[log_index], feature_portfolio)
    return x


def compute_single_feature(log_path, feature_name):
    globals.set_progress_current_feature_name_and_percentage(
        log_path, feature_name)

    # Check if the feature name is valid
    if feature_name in feature_functions:
        # Call the corresponding feature function
        ret = feature_functions[feature_name](log_path)
        return ret
    else:

        print("Invalid feature name")
        print(feature_name)
        return None


def get_total_feature_functions_dict():
    mtl_dict = get_mtl_feature_functions_dict()
    fig4pm_dict = get_fig4pm_feature_functions_dict()
    own_features_dict = get_own_features_dict()

    feature_dict = {**mtl_dict, **fig4pm_dict, **own_features_dict}
    features_to_remove = get_removed_features_list()
    filtered_feature_dict = {key: feature_dict[key]
                             for key in feature_dict if key not in features_to_remove}

    store_cache_variable(list(filtered_feature_dict.keys()),
                         "./constants/feature_portfolio.pk")
    return filtered_feature_dict


feature_functions = get_total_feature_functions_dict()
if __name__ == "__main__":

    feature_dict = get_total_feature_functions_dict()

    feature_list = list(feature_dict.keys())

    directories = [os.path.join("../logs/real_life_logs", d) for d in os.listdir(
        "../logs/real_life_logs") if os.path.isdir(os.path.join("../logs/real_life_logs", d))]

    for log_dir in directories:
        log_log_collection_info(log_dir)
        input("next ?")
    """"
    mtl_dict = get_mtl_feature_functions_dict()
    fig4pm_dict = get_fig4pm_feature_functions_dict()
    own_features_dict = get_own_features_dict()
    feature_functions = {**mtl_dict, **fig4pm_dict, **own_features_dict}
    globals.algorithm_portfolio = ["alpha", "inductive"]
    log_paths = gather_all_xes(
        "../logs/training") + gather_all_xes("../logs/testing") + gather_all_xes("../logs/modified_eventlogs")
    #globals.feature_portfolio = list(feature_functions.keys())
    for log_path in log_paths:
        failed_features = []
        for feature_name in own_features_dict:
            try:
                read_single_feature(log_path, feature_name)
            except Exception as e:
                print(":(")
    """
