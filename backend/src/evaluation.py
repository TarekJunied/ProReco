import sys
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import numpy as np
import globals
from utils import get_all_ready_logs, split_data
from recommender import classification
from filehelper import gather_all_xes, select_smallest_k_logs
from measures import read_target_entries, read_target_entry, read_target_vector
from features import read_feature_matrix
from init import init_testing_logs


def evaluate_measure_accuracy(training_logs, testing_logs, measure_name, classification_method="knn"):
    y_true = [None]*(len(training_logs))
    y_pred = [None]*(len(testing_logs))

    x_train = read_feature_matrix(ready_for_trainingpaths)
    y_train = read_target_vector(ready_for_trainingpaths, measure_name)

    print(f"We have {len(training_logs)} training logs")
    print(f"We have {len(testing_logs)} testing logs")
    input(measure_name)
    for i in range(len(testing_logs)):
        y_true[i] = read_target_entry(
            testing_logs[i], measure_name)
        y_pred[i] = classification(
            testing_logs[i], x_train, y_train, classification_method)

    precision_per_class = precision_score(
        y_true, y_pred, average=None, labels=globals.algorithm_portfolio)
    recall_per_class = recall_score(
        y_true, y_pred, average=None, labels=globals.algorithm_portfolio)
    f1_score_per_class = f1_score(
        y_true, y_pred, average=None, labels=globals.algorithm_portfolio)

    os.system("clear")
    
    print("ACCURACY: ", accuracy_score(y_true, y_pred))
    print("PRECISION: ", precision_per_class)
    print("RECALL: ", recall_per_class)
    print("F1 SCORE: ", f1_score_per_class)


if __name__ == "__main__":
    sys.setrecursionlimit(5000)

    selected_measure = "runtime"

    testing_logpaths = gather_all_xes("../logs/testing/")
    training_logppaths = gather_all_xes("../logs/training/")

    # selected_logs = testing_logpaths + \
    #        select_smallest_k_logs(70, "../logs/training")
    # init_testing_logs(selected_logs, [selected_measure])

    ready_for_testingpaths = get_all_ready_logs(
        testing_logpaths, selected_measure)
    ready_for_trainingpaths = get_all_ready_logs(
        training_logppaths, selected_measure)


    selected_measures = ["node_arc_degree", "no_total_elements",
                         "used_memory", "pm4py_simplicity", "runtime"]

    for measure_name in selected_measures:
        evaluate_measure_accuracy(ready_for_trainingpaths,
                                  ready_for_testingpaths, measure_name, "knn")
