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
from utils import read_logs,read_models,split_list,get_all_ready_logs,filter_infrequent_logs,read_log,split_data
from measures import read_target_entry,read_target_entries
from init import *

def classification(new_log_path,X,y):
    knn = KNeighborsClassifier(n_neighbors=4, weights='uniform', algorithm='auto',
                               p=2, metric="minkowski")
    knn.fit(X, y)

    prediction = knn.predict(read_feature_vector(new_log_path))

    globals.predictions[new_log_path] = prediction

    print("predicition is ", prediction)

    return prediction


if __name__ == "__main__":
    print("hi")

    