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
from features import read_feature_matrix,read_feature_vector,feature_no_total_traces
from utils import read_logs,read_models,split_list,get_all_ready_logs,filter_infrequent_logs,read_log
from measures import read_target_entry,read_target_entries
from init import *


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
    #num_cores = multiprocessing.cpu_count()
    #pool = multiprocessing.Pool(processes=num_cores)
    
    training_log_paths = gather_all_xes("./LogGenerator/logs")
    testing_logpaths = gather_all_xes("../logs/logs_in_xes")

    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_cores)


    input_data = []

    for log_path in testing_logpaths:
        input_data += [(log_path,"token_precision")]

    results = pool.starmap(init_log, input_data)

    print(results)
    pool.close()
    pool.join()

    