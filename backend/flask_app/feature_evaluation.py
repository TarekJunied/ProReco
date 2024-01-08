import sys
from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import os
import numpy as np
import globals
from datetime import datetime
from utils import load_cache_variable, split_data, get_log_name, read_log, generate_cache_file, store_cache_variable
from flask_app.features.removed_features import get_removed_features_list
from flask_app.features.removed_features import get_removed_features_list
from flask_app.features.fig4pm_features.fig4pm_interface import get_fig4pm_feature_functions_dict
from flask_app.features.own_features import get_own_features_dict
from flask_app.features.mtl_features.mtl_feature_interface import get_mtl_feature_functions_dict
from flask_app.feature_selection import regression_read_optimal_features
from regressors import read_fitted_regressor
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import time


def set_feature_descriptions(feature_list):
    print("Write descriptions for the following features")
    for feature in feature_list:
        #        x = input(feature)
        store_cache_variable(
            "hi", f"./constants/feature_information/descriptions/{feature}.pk")


def read_feature_description(feature):
    return load_cache_variable(
        f"./constants/feature_information/descriptions/{feature}.pk")


def get_feature_source(feature):
    removed_features = get_removed_features_list()
    fig4pm_features = get_fig4pm_feature_functions_dict()
    own_features = get_own_features_dict()
    mtl_features = get_mtl_feature_functions_dict()

    if feature in removed_features:
        return "removed features"
    if feature in fig4pm_features:
        return "fig4pm"
    if feature in own_features:
        return "developed for proreco"
    if feature in mtl_features:
        return "mtl_features"
    else:
        return "unknown"


def get_feature_importance_dict():
    cache_file_path = "./constants/feature_importance_dict.pk"
    try:
        ret = load_cache_variable(cache_file_path)
    except Exception:
        ret = {}
        for feature in globals.feature_portfolio:
            for discovery_algorithm in globals.algorithm_portfolio:
                for measure in globals.measure_portfolio:
                    cache_file_path = f"{globals.flask_app_path}/cache/optimal_features_lists/regression/{globals.regression_method}/optimal_features_{discovery_algorithm}_{measure}.pk"
                    cur_optimal_feature_list = load_cache_variable(
                        cache_file_path)
                    if feature in cur_optimal_feature_list:
                        cur_regressor = read_fitted_regressor(
                            globals.regression_method, discovery_algorithm, measure, [])
                        feature_importances = cur_regressor.feature_importances_
                        feature_index = regression_read_optimal_features(
                            [], "xgboost", discovery_algorithm, measure, []).index(feature)
                        single_feature_importance = feature_importances[feature_index]
                        ret[discovery_algorithm, measure,
                            feature] = single_feature_importance

                    else:
                        ret[discovery_algorithm, measure, feature] = 0
        store_cache_variable(ret, cache_file_path)
    return ret


def get_most_important_regressor_string(feature):
    feature_importance_dict = get_feature_importance_dict()
    feature_specific_dict = {f"{discovery_algorithm}_{measure}_regressor": feature_importance_dict[discovery_algorithm, measure, feature]
                             for discovery_algorithm in globals.algorithm_portfolio
                             for measure in globals.measure_portfolio}
    key_with_highest_value = max(
        feature_specific_dict, key=feature_specific_dict.get)
    return key_with_highest_value


def get_number_of_regressors_string(feature):
    feature_importance_dict = get_feature_importance_dict()
    feature_specific_dict = {f"{discovery_algorithm}_{measure}_regressor": feature_importance_dict[discovery_algorithm, measure, feature]
                             for discovery_algorithm in globals.algorithm_portfolio
                             for measure in globals.measure_portfolio if feature_importance_dict[discovery_algorithm, measure, feature] > 0}
    return len(feature_specific_dict)


def read_feature_importance_across_all_regressors(feat):
    feature_importance_dict = get_feature_importance_dict()
    feature_specific_dict = {f"{discovery_algorithm}_{measure}_regressor": feature_importance_dict[discovery_algorithm, measure, feat]
                             for discovery_algorithm in globals.algorithm_portfolio
                             for measure in globals.measure_portfolio}
    total_sum = 0
    for key in feature_specific_dict:
        total_sum += feature_specific_dict[key]
    return total_sum


def get_total_feature_importance_ranking(feature):
    feature_importance_vals = {feat: read_feature_importance_across_all_regressors(
        feat) for feat in globals.feature_portfolio}
    sorted_features = sorted(
        feature_importance_vals.items(), key=lambda item: item[1], reverse=True)
    for rank, (feat, _) in enumerate(sorted_features, start=1):
        if feat == feature:
            # Step 4: Format the rank alongside the total number of features
            return f"{rank}/{len(globals.feature_portfolio)}"

    # In case the feature is not found or another error occurs
    return "Feature not found or error in calculation"


def compute_single_feature_information_dict(feature):
    ret_dict = {}
    # short description:
    # from :
    # optional if used in any regressors
    # used in how many regressors ?
    # most_important_regressor: regressor this feature is most important for
    # feature importance ranking in that regressor
    # total feature ranking: out of all used features
    ret_dict["description"] = read_feature_description(feature)
    ret_dict["from"] = get_feature_source(feature)
    ret_dict["no_regressors"] = get_number_of_regressors_string(feature)
    ret_dict["most_important_regressor"] = get_most_important_regressor_string(
        feature)
    ret_dict["feature_ranking"] = get_total_feature_importance_ranking(feature)
    ret_dict["feature_importance_points"] = read_feature_importance_across_all_regressors(
        feature)
    return ret_dict


def read_single_feature_information_dict(feature):
    cache_file_path = f"./constants/feature_information/{feature}_info.pk"
    try:
        ret = load_cache_variable(cache_file_path)
    except Exception:
        generate_cache_file(cache_file_path)
        ret = compute_single_feature_information_dict(feature)
        store_cache_variable(ret, cache_file_path)


if __name__ == "__main__":
    sys.setrecursionlimit(5000)
    compute_single_feature_information_dict(sys.argv[1])
