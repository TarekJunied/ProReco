import matplotlib.pyplot as plt
import pandas as pd
import globals
import numpy as np
import subprocess
import os
import pm4py
from utils import read_logs, read_models, get_all_ready_logs
from sklearn.metrics import accuracy_score
from filehelper import gather_all_xes, get_all_ready_logs
from feature_controller import read_feature_matrix, read_feature_vector
from feature_selection import read_optimal_features
from measures import read_binary_classification_target_vector, read_target_entry
from init import *
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, ExtraTreesClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import RidgeClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import PassiveAggressiveClassifier
from lime import lime_tabular
from sklearn.tree import plot_tree


def get_all_pairs_of_algorithms(algorithm_portfolio):
    ret = []
    n = len(algorithm_portfolio)
    for i in range(n):
        for j in range(i+1, n):
            ret += [(algorithm_portfolio[i], algorithm_portfolio[j])]

    return ret


def actual_binary_classification(log_path, algorithm_a, algorithm_b, measure):
    return read_target_entry(log_path, measure, [algorithm_a, algorithm_b])


def predicted_binary_classification(log_path, algorithm_a, algorithm_b, measure, ready_training, feature_portfolio, binary_classification_method):

    clf = read_fitted_binary_classifier(
        binary_classification_method, algorithm_a, algorithm_b, measure, ready_training, feature_portfolio)

    predictions = clf.predict(read_feature_vector(log_path, feature_portfolio))

    return predictions[0]


def compute_fitted_binary_classifier(algorithm_a, algorithm_b, measure, ready_training, feature_portfolio, binary_classification_method):
    x_train = read_feature_matrix(ready_training, feature_portfolio)
    y_train = read_binary_classification_target_vector(
        ready_training, measure, algorithm_a, algorithm_b)

    y_train[0] = algorithm_a
    y_train[1] = algorithm_b

    classifiers = {
        "decision_tree": DecisionTreeClassifier(),
        "knn": KNeighborsClassifier(n_neighbors=9),
        "svm": SVC(probability=True),
        "random_forest": RandomForestClassifier(),
        "logistic_regression": LogisticRegression(),
        "gradient_boosting": GradientBoostingClassifier(n_estimators=100),
        "xgboost": XGBClassifier(use_label_encoder=False, eval_metric='logloss', objective='binary:logistic'),
        "catboost": CatBoostClassifier(),
        "mlp": MLPClassifier(),
        "adaboost": AdaBoostClassifier(),
        "extra_trees": ExtraTreesClassifier(),
        "gaussian_nb": GaussianNB(),
        "ridge": RidgeClassifier(),
        "sgd": SGDClassifier(),
        "passive_aggressive": PassiveAggressiveClassifier()
    }

    clf = classifiers[binary_classification_method]
    clf = clf.fit(x_train, y_train)

    return clf


def read_fitted_binary_classifier(binary_classification_method, algorithm_a, algorithm_b, measure, ready_training, feature_portfolio):
    storage_path = f"./cache/binary_classifiers/{binary_classification_method}"
    if not os.path.exists(storage_path):
        os.mkdir(storage_path)
    classifier_filepath = f"{storage_path}/{measure}_{algorithm_a}_{algorithm_b}_{binary_classification_method}.pkl"
    try:
        ret = load_cache_variable(classifier_filepath)
    except Exception:
        print("Binary classifier doesn't exist yet. Computing classifier now")
        ret = compute_fitted_binary_classifier(
            algorithm_a, algorithm_b, measure, ready_training, feature_portfolio, binary_classification_method)
        store_cache_variable(ret, classifier_filepath)
    return ret


if __name__ == "__main__":
    globals.algorithm_portfolio = ["alpha", "heuristic",
                                   "inductive", "ILP", "split"]

    classifiers = {
        "decision_tree": DecisionTreeClassifier(),
        "knn": KNeighborsClassifier(n_neighbors=9),
        "svm": SVC(probability=True),
        "random_forest": RandomForestClassifier(),
        "logistic_regression": LogisticRegression(),
        "gradient_boosting": GradientBoostingClassifier(n_estimators=100),
        "xgboost": XGBClassifier(use_label_encoder=False, eval_metric='logloss', objective='binary:logistic'),
        "mlp": MLPClassifier(),
        "adaboost": AdaBoostClassifier(),
        "extra_trees": ExtraTreesClassifier(),
        "gaussian_nb": GaussianNB(),
        "ridge": RidgeClassifier(),
        "sgd": SGDClassifier(),
        "passive_aggressive": PassiveAggressiveClassifier()
    }

    binary_classification_methods = list(classifiers.keys())

    feature_dict = get_total_feature_functions_dict()

    feature_list = list(feature_dict.keys())

    globals.selected_features = feature_list
    globals.measures_list = ["token_fitness", "token_precision",
                             "no_total_elements", "generalization", "pm4py_simplicity"]

    globals.selected_features = feature_list

    algorithm_portfolio = globals.algorithm_portfolio

    algorithm_pairs = get_all_pairs_of_algorithms(algorithm_portfolio)

    all_logs = gather_all_xes("../logs/testing")
    ready_logs = get_all_ready_logs(
        all_logs, feature_list, algorithm_portfolio, globals.measures_list)[:50]

    for log_path in ready_logs:
        for binary_classification_method in binary_classification_methods:
            for measure in globals.measures_list:
                for (algorithm_a, algorithm_b) in algorithm_pairs:
                    actual = actual_binary_classification(
                        log_path, algorithm_a, algorithm_b, measure)
                    predicted = predicted_binary_classification(
                        log_path, algorithm_a, algorithm_b, measure, ready_logs, feature_list, binary_classification_method)
