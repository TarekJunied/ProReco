from utils import read_logs, read_models,  get_all_ready_logs, read_log, split_data
from filehelper import gather_all_xes, get_all_ready_logs, get_all_ready_logs_multiple
from features import read_feature_matrix, read_feature_vector, feature_no_total_traces
from measures import read_target_entry, read_target_entries, read_measure_entry
from init import *
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import multiprocessing
import globals
import numpy as np
import os
import pm4py
import sys
project_dir = '/rwthfs/rz/cluster/home/qc261227/Recommender/RecommenderSystem/backend/src'
# Add the project directory to sys.path
sys.path.append(project_dir)

label_to_index = {label: index for index,
                  label in enumerate(globals.algorithm_portfolio)}


all_labels = list(label_to_index.keys())


#TODO: tailor this again to backend
def classification(log_path, classification_method,measure_name):

    ready_training = list(globals.training_log_paths.keys())

    x_train = read_feature_matrix(ready_training)

    y_train = read_target_vector(ready_training, measure_name)

    if classification_method == "decision_tree":
        clf = DecisionTreeClassifier()
    elif classification_method == "knn":
        clf = KNeighborsClassifier(n_neighbors=9)
    elif classification_method == "svm":
        clf = SVC(probability=True)
    elif classification_method == "random_forest":
        clf = RandomForestClassifier()
    elif classification_method == "logistic_regression":
        clf = LogisticRegression(max_iter=1000000)
    elif classification_method == "gradient_boosting":
        clf = GradientBoostingClassifier()
    else:
        raise ValueError(
            f"Invalid classification method: {classification_method}")

    clf = clf.fit(x_train, y_train)

    predictions = clf.predict(read_feature_vector(log_path))



    return predictions[0]
  


def final_prediction(log_path, measure_weight):
    """returns the predicted rankings
    1st place ILP => ret["ILP"] = 1
    Args:
        log_path: _description_
        measure_weight: _description_

    Returns:
        _description_
    """
    log_paths = get_all_ready_logs_multiple(
        gather_all_xes("../logs/experiments"))

    x_train = read_feature_matrix(log_paths)
    y_train = [None]*len(log_paths)

    for i in range(len(y_train)):
        my_dict = final_rankings(
            log_paths[i], measure_weight)
        y_train[i] = max(my_dict, key=my_dict.get)

    return classification(log_path, x_train, y_train, "decision_tree")[1]


def final_rankings(log_path, measure_weight):
    rank_list = {}
    for disco_algorithm in globals.algorithm_portfolio:
        rank_list[disco_algorithm] = score(
            log_path, disco_algorithm, measure_weight)
    return rank_list


def measure_score(log_path, discovery_algorithm, measure):
    rank_list = {}
    for disco_algorithm in globals.algorithm_portfolio:
        rank_list[disco_algorithm] = read_measure_entry(
            log_path, disco_algorithm, measure)

    if str(globals.measures[measure]) == "min":
        sorted_items = sorted(
            rank_list.items(), reverse=True, key=lambda item: item[1])
    elif str(globals.measures[measure]) == "max":
        sorted_items = sorted(
            rank_list.items(), reverse=False, key=lambda item: item[1])
    else:
        print(globals.measures[measure] == "min")
    sorted_keys_list = [item[0] for item in sorted_items]
    return sorted_keys_list.index(discovery_algorithm) + 1


def score(log_path, discovery_algorithm, measure_weight):
    """ computes the score used for the final ranking

    Args:
        log_path: the log path used
        discovery_algorithm: the discovery algorithm used
        measure_weight: a dictionary that uses the measure names as key and 
        the weights of the measures selected as values
    """
    total_score = 0
    i = 0
    for measure in globals.measures:
        total_score += measure_weight[measure] * \
            measure_score(log_path, discovery_algorithm, measure)

    return total_score


if __name__ == "__main__":

    
    init()

    ready_testing = list(globals.testing_log_paths.keys())

    print(classification(ready_testing[0],"knn","token_precision"))
    input("stop")
    logs = get_all_ready_logs_multiple(gather_all_xes("../logs/experiments"))

    log_path = logs[0]

    measure_weight = {}

    for measure in globals.measures:
        measure_weight[measure] = 0

    measure_weight["runtime"] = 0.5
    measure_weight["token_precision"] = 0.5

    print(final_prediction(log_path, measure_weight))
