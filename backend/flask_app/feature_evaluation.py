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
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error
from utils import load_cache_variable, split_data, get_log_name, read_log
from filehelper import gather_all_xes, get_all_ready_logs, clear_cached_classifiers, clear_cached_regressors, clear_cached_binary_classifiers
from measures import read_measure_entry, read_target_entry, read_binary_classification_target_entry, read_regression_target_vector
from feature_controller import read_feature_matrix, read_single_feature, get_total_feature_functions_dict
from regressors import get_regression_based_classification_methods, regression, regression_based_classification, init_regressors
from classifiers import classification
from multiobjective import predicted_regression_based_scalarization, actual_regression_based_scalarization
from flask_app.features.removed_features import get_removed_features_list
from init import init_given_parameters, filter_instances_with_nan, reset_all_cached_predictors
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
import os
from datetime import datetime
import time


def plot_feature_importance(regression_method):
    initial_features = globals.feature_portfolio


if __name__ == "__main__":
    sys.setrecursionlimit(5000)

    all_logs = gather_all_xes("../logs")
    ready_logs = get_all_ready_logs(
        all_logs, globals.feature_portfolio, globals.algorithm_portfolio, globals.measure_portfolio)
    ready_training, ready_testing = split_data(ready_logs)

    init_given_parameters(ready_logs, globals.algorithm_portfolio,
                          globals.feature_portfolio, globals.measure_portfolio)
    # CHANGE IT TO ONLY LOAD NEEDED FEATURES, ONCE OPTIMAL FEATURE SETS ARE COMPUTED DO THAT
    no_cv = 5
    measure_weights_dict_list = [{"token_fitness": 0.5, "token_precision": 0.5, "pm4py_simplicity": 0, "generalization": 0},
                                 {"token_fitness": 0.5, "token_precision": 0,
                                  "pm4py_simplicity": 0.5, "generalization": 0},
                                 {"token_fitness": 0.5, "token_precision": 0,
                                  "pm4py_simplicity": 0, "generalization": 0.5},
                                 {"token_fitness": 0, "token_precision": 0.5,
                                  "pm4py_simplicity": 1, "generalization": 0},
                                 {"token_fitness": 0, "token_precision": 1,
                                  "pm4py_simplicity": 0.5, "generalization": 0},
                                 {"token_fitness": 0, "token_precision": 0.75,
                                  "pm4py_simplicity": 1, "generalization": 0},
                                 {"token_fitness": 0, "token_precision": 1,
                                  "pm4py_simplicity": 0, "generalization": 0.75},
                                 {"token_fitness": 0, "token_precision": 0,
                                  "pm4py_simplicity": 1, "generalization": 1}]
