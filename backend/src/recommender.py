project_dir = '/rwthfs/rz/cluster/home/qc261227/Recommender/RecommenderSystem/backend/src'
import sys
# Add the project directory to sys.path
sys.path.append(project_dir)


import pm4py
import os
import numpy as np
import sys
import globals
import multiprocessing
from filehelper import gather_all_xes, select_smallest_k_logs
from sklearn.neighbors import KNeighborsClassifier
from features import read_feature_matrix,read_subset_features,read_feature_vector
from utils import read_logs, pickle_retrieve, pickle_dump, load_all_globals_from_cache, load_target_vector_into_y, read_models, read_model, split_list
from measures import read_target_entry
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

    prediction = knn.predict(read_feature_vector(new_log_path))

    globals.predictions[new_log_path] = prediction

    print("predicition is ", prediction)

    return prediction


if __name__ == "__main__":
    sys.setrecursionlimit(5000)



    all_log_paths = gather_all_xes("./LogGenerator/logs")

    number_of_processes = len(all_log_paths)

    list_of_log_paths = split_list(all_log_paths, number_of_processes)

    # with multiprocessing.Pool(processes=len(all_log_paths)) as pool:
    #    pool.map(read_models, list_of_log_paths)

    node_id = int(os.environ.get("SLURM_NODEID", 0))
    total_nodes = int(os.environ.get("SLURM_NNODES", 1))
    total_files = len(all_log_paths)


    # Calculate the number of files each node should process
    files_per_node = total_files // total_nodes
    remainder = total_files % total_nodes

    print("Entered python now. Some statistics:")
    print("Number of nodes: ",total_nodes)
    print("Number of files: ",total_files)
    print("Files per node: ", files_per_node)


    # Calculate the start and end indices for this node's files
    start_index = node_id * files_per_node + min(node_id, remainder)
    end_index = start_index + files_per_node + \
        (1 if node_id < remainder else 0)

    # Extract the subset of files for this node
    selected_log_paths = all_log_paths[start_index:end_index]

    #read_models(selected_log_paths)
    globals.X = np.empty((len(all_log_paths),
                         len(globals.selected_features)))

    #read_subset_features(selected_log_paths)
    read_feature_matrix(all_log_paths)


    testing_logpaths = gather_all_xes("../logs/logs_in_xes")

    globals.y = [None] * len(all_log_paths)
    for i in range(len(all_log_paths)):
        globals.y[i] = read_target_entry(all_log_paths[i],"token_precision")


    correct = 0
    for log_path in testing_logpaths:
        prediction = classification(log_path)
        print(f"we predict for {log_path}: {prediction}")
        actual = read_target_entry(log_path, "token_precision")
        print(f"but actual is: ", actual)
        if actual == prediction:
            correct+=1
    print("total correct: ",correct )
    print(correct/len(testing_logpaths))

    #TODO parallelize computing of the feature matrix
