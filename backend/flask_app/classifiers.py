# import shap
import matplotlib.pyplot as plt
import pandas as pd
import globals
import numpy as np
import subprocess
import os
import pm4py
from xgboost import XGBClassifier
from filehelper import gather_all_xes, get_all_ready_logs
from feature_controller import read_feature_matrix, read_feature_vector
from measures import read_measure_entry, read_regression_target_vector
from init import *
from autofolio_interface import autofolio_classification
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from lime import lime_tabular
from sklearn.tree import plot_tree


def compute_fitted_classifier(classification_method, measure_name, ready_training, feature_portfolio):
    x_train = read_feature_matrix(ready_training, feature_portfolio)
    y_train = read_classification_target_vector(
        ready_training, measure_name, globals.algorithm_portfolio)

    if classification_method == "decision_tree":
        clf = DecisionTreeClassifier()
    elif classification_method == "knn":
        clf = KNeighborsClassifier(n_neighbors=9)
    elif classification_method == "svm":
        clf = SVC(probability=True)
    elif classification_method == "random_forest":
        clf = RandomForestClassifier()
    elif classification_method == "logistic_regression":
        clf = LogisticRegression()
    elif classification_method == "gradient_boosting":
        clf = GradientBoostingClassifier(n_estimators=100)
    elif classification_method == "xgboost":
        clf = XGBClassifier(use_label_encoder=False, eval_metric='logloss',
                            objective='multi:softprob', num_class=len(globals.algorithm_portfolio))
    else:
        raise ValueError(
            f"Invalid classification method: {classification_method}")

    clf = clf.fit(x_train, y_train)

    return clf


def read_fitted_classifier(classification_method, measure_name, ready_training, feature_portfolio):
    classifier_filepath = f"./cache/classifiers/{measure_name}_{classification_method}.pkl"
    try:
        ret = load_cache_variable(classifier_filepath)

    except Exception:
        print("Classifier doesn't exist yet. Computing classifier now")

        ret = compute_fitted_classifier(
            classification_method, measure_name, ready_training, feature_portfolio)

        store_cache_variable(ret, classifier_filepath)

    return ret
