import pm4py
import os
import numpy as np
import globals
from filehelper import gather_all_xes, select_smallest_k_logs
from sklearn.neighbors import KNeighborsClassifier
from features import compute_features_of_log, init_feature_matrix
from measures import init_target_vector, init_target_entry
from utils import read_logs, pickle_retrieve, pickle_dump, load_all_globals_from_cache, load_target_vector_into_y, read_models


def init():
    globals.training_logs_paths = select_smallest_k_logs(
        10, "./LogGenerator/logs")

    read_logs("./LogGenerator/logs")

    print("Now finished reading logs")

    read_models("./LogGenerator/logs")

    print("Now finished computing models and runtime")
    log_paths = gather_all_xes("./LogGenerator/logs")

    init_feature_matrix(log_paths, globals.selected_features)
    # print("Now finished computing feature matrix")

    # init_target_vector(globals.selected_measure)
    # print("now finished computing target_vector")
    # print(globals.y)


def classification(new_log_path):
    knn = KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto',
                               p=2, metric="minkowski")
    knn.fit(globals.X, globals.y)

    prediction = knn.predict(compute_features_of_log(new_log_path))

    globals.predictions[new_log_path] = prediction

    print("predicition is ", prediction)

    return prediction


# init()
read_models("./LogGenerator/logs")


""""
correct = 0
log_paths = gather_all_xes("../logs/logs_in_xes")
n = len(log_paths)
for i in range(5):
    log_path = log_paths[i]
    init_target_entry(
        log_paths[i], i, globals.selected_measure)
    prediction = classification(log_path)

    if globals.target_vectors[log_path, globals.selected_measure] == prediction:
        correct += 1
        print("correct")
        print(correct)
        print(n)
        print(correct/n)
    else:
        print("wrong")
        print(correct)
        print(n)
        print(correct/n)

print(correct)
print(n)
print(correct/n)
"""
