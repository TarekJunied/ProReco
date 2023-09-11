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

def classification(new_log_path,X,y):
    knn = KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto',
                               p=2, metric="minkowski")
    knn.fit(X, y)

    prediction = knn.predict(read_feature_vector(new_log_path))

    globals.predictions[new_log_path] = prediction

    print("predicition is ", prediction)

    return prediction


if __name__ == "__main__":
    sys.setrecursionlimit(5000)
    
    training_log_paths = gather_all_xes("./LogGenerator/logs")
    testing_logpaths = gather_all_xes("../logs/logs_in_xes")

    proc_disc = gather_all_xes("../logs/Process_Discovery_Contests/testing")
    input(len(proc_disc))
    init_testing_logs(proc_disc,["token_precision"])
    input("done with proc_disc")
    ready_training = get_all_ready_logs(training_log_paths,"token_precision")

    ready_testing = get_all_ready_logs(testing_logpaths,"token_precision")

    x = read_feature_matrix(ready_training)
    
    y = [None]*len(ready_training)
    i = 0
    for log_path in ready_training:
        y[i] = read_target_entry(log_path,"token_precision")
        i += 1

    correct = 0
    for log_path in ready_testing:
        actual = read_target_entry(log_path,"token_precision")
        prediction = classification(log_path, x, y)[0]
        print("ACUTAL: ", actual)
        print("PREDICTION: ", prediction)

        if actual == prediction: 
            correct +=1
            print("Correct")
        else:
            print("Wrong")

    print("TOTAL CORRECT: ", correct)
    print("OUT OF ", len(ready_testing))
    print(correct/len(ready_testing))

   

    