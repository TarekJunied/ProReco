import pm4py
from filehelper import gather_all_xes, select_smallest_k_logs
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from globals import log_paths, algorithm_portfolio, selected_features, logs, measures
from features import (
    feature_avg_event_repetition_intra_trace,
    compute_features_of_log,
    compute_feature,
    feature_density, feature_causality_strength, feature_length_one_loops,
)
from measures import compute_measure

from utils import read_log, read_model, load_all_logs_from_cache


def compute_all_models():
    for discovery_algorithm in algorithm_portfolio:
        for log_path in log_paths:
            read_model(log_path, discovery_algorithm)


def init_feature_matrix():
    global X
    X = np.empty((len(log_paths), len(selected_features)))
    for log_index in range(len(log_paths)):
        for feature_index in range(len(selected_features)):
            X[log_index, feature_index] = compute_feature(
                log_index, feature_index)


def init_target(log_path, log_index):
    global y
    cur_fit = float("-inf")
    for discovery_algorithm in algorithm_portfolio:
        algo_fit = precision_token_based_replay(log_path, discovery_algorithm)
        if algo_fit > cur_fit:
            cur_fit = algo_fit
            y[log_index] = discovery_algorithm


def init():
    global y, X, log_paths
    load_all_logs_from_cache()

    log_paths = select_smallest_k_logs(3)

    X = np.empty((len(log_paths), len(selected_features)))
    y = [None] * len(log_paths)

    print("now finished loading all logs from cache")

    init_feature_matrix()
    print("now finished initializing feature matrix")
    # determine the best algorithm for all logs
    for i in range(len(log_paths)):
        init_target(log_paths[i], i)

    print("now finished initializing target vector")

    matrix_string = np.array2string(X, separator=', ', formatter={
                                    'all': lambda x: f'{x:.2f}'}, suppress_small=True)
    print("now printing feature matrix")
    print(matrix_string)
    print("now printing y:")
    print(y)


def classification(new_log_path):
    knn = KNeighborsClassifier(n_neighbors=1, weights='uniform', algorithm='auto',
                               p=2, metric="minkowski")
    knn.fit(X, y)

    prediction = knn.predict(compute_features_of_log(new_log_path))

    print("prediciton is ", prediction)

    return prediction


log_paths = gather_all_xes("./")
log = read_log(log_paths[1])
for measure_name in measures:
    print(compute_measure(log_paths[1], "alpha", measure_name))
