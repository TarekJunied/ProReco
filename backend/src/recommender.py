from utils import read_logs, read_models, split_list, get_all_ready_logs, read_log, split_data
from features import read_feature_matrix, read_feature_vector, feature_no_total_traces
from measures import read_target_entry, read_target_entries
from init import *
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from filehelper import gather_all_xes, select_smallest_k_logs
import multiprocessing
import globals
import numpy as np
import os
import pm4py
import sys
project_dir = '/rwthfs/rz/cluster/home/qc261227/Recommender/RecommenderSystem/backend/src'
# Add the project directory to sys.path
sys.path.append(project_dir)

def classification(log_path,X,y,classification_method):
    if classification_method == "decision_tree":
        return classification_decision_tree(log_path, X, y)
    if classification_method == "knn":
        return classification_knn(log_path, X, y)



def classification_decision_tree(log_path, X, y):
    clf = tree.DecisionTreeClassifier()

    clf = clf.fit(X, y)

    prediction = clf.predict(read_feature_vector(log_path))

    print("predicition is ", prediction)

    return prediction[0]


def classification_knn(log_path, X, y):
    knn = KNeighborsClassifier(n_neighbors=4, weights='uniform', algorithm='auto',
                               p=2, metric="minkowski")
    knn.fit(X, y)

    prediction = knn.predict(read_feature_vector(log_path))

    print("predicition is ", prediction)

    return prediction[0]


if __name__ == "__main__":
    print("hi")
