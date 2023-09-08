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
from features import read_feature_matrix,read_feature_vector
from utils import read_logs, pickle_retrieve, pickle_dump, load_all_globals_from_cache, load_target_vector_into_y, read_models, read_model, split_list,read_log
from measures import read_target_entry,read_target_entries
# Fitness measures


def init():
    log_paths = gather_all_xes("./LogGenerator/logs")
    read_models(log_paths)

    print("Now finished reading logs")

    read_models(log_paths)

    print("Now finished computing models and runtime")
   

    x = read_feature_matrix(log_paths)
    print("Now finished computing feature matrix")

  
    # print("now finished computing target_vector")
    # print(globals.y)


def classification(new_log_path,X,y):
    knn = KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto',
                               p=2, metric="minkowski")
    knn.fit(globals.X, globals.y)

    prediction = knn.predict(read_feature_vector(new_log_path))

    globals.predictions[new_log_path] = prediction

    print("predicition is ", prediction)

    return prediction


if __name__ == "__main__":
    sys.setrecursionlimit(5000)



    training_log_paths = gather_all_xes("./LogGenerator/logs")
    testing_logpaths = gather_all_xes("../logs/logs_in_xes")



    node_id = int(sys.argv[1])
    total_nodes = int(sys.argv[2])


    list_of_lists = split_list(testing_logpaths, total_nodes)
    selected_logpaths = list_of_lists[node_id]
    print("Hi I am node: ", node_id)
    print(selected_logpaths)
    read_logs(selected_logpaths)
    read_models(selected_logpaths)
    read_target_entries(selected_logpaths, "token_precision")

    print("CODE 23092002")    
    