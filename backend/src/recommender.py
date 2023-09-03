import pm4py
import os
import numpy as np
import sys
import globals
from filehelper import gather_all_xes, select_smallest_k_logs
from sklearn.neighbors import KNeighborsClassifier
from features import read_feature_matrix
from utils import read_logs, pickle_retrieve, pickle_dump, load_all_globals_from_cache, load_target_vector_into_y, read_models, read_model, split_list
# Fitness measures


def init():

    read_models("./LogGenerator/logs")

    print("Now finished reading logs")

    read_models("./LogGenerator/logs")

    print("Now finished computing models and runtime")
    log_paths = gather_all_xes("./LogGenerator/logs")

    read_feature_matrix(log_paths)
    print("Now finished computing feature matrix")

    # read_target_vector(globals.selected_measure)
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


if __name__ == "__main__":
    sys.setrecursionlimit(5000)

    all_log_paths = gather_all_xes("./LogGenerator/logs")

    # list_of_log_paths = split_list(all_log_paths, number_of_nodes)

    node_id = int(os.environ.get("SLURM_NODEID", 0))
    total_nodes = int(os.environ.get("SLURM_NNODES", 1))
    total_files = len(all_log_paths)

    # Calculate the number of files each node should process
    files_per_node = total_files // total_nodes
    remainder = total_files % total_nodes

    # Calculate the start and end indices for this node's files
    start_index = node_id * files_per_node + min(node_id, remainder)
    end_index = start_index + files_per_node + \
        (1 if node_id < remainder else 0)

    # Extract the subset of files for this node
    selected_log_paths = all_log_paths[start_index:end_index]

    read_models(selected_log_paths)
