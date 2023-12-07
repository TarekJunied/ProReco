import multiprocessing
import globals
import numpy as np
import subprocess
import os
import re
import pm4py
from utils import read_logs, read_models,  get_all_ready_logs
from filehelper import gather_all_xes, get_all_ready_logs, get_all_ready_logs_multiple
from features import read_feature_matrix, read_feature_vector, feature_no_total_traces,space_out_feature_vector_string
from measures import read_measure_entry
from init import *
from autofolio_interface import  autofolio_classification
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV




label_to_index = {label: index for index,
                  label in enumerate(globals.algorithm_portfolio)}


all_labels = list(label_to_index.keys())
def activate_smac_env():
    subprocess.run("conda run -n SMAC",shell=True)









def read_fitted_classifier(classification_method,measure_name,ready_training):
    classifier_filepath = f"./classifiers/{measure_name}_{classification_method}.pkl"
    try:
        clf = load_cache_variable(classifier_filepath)
    except Exception:
        print("Classifier doesn't exist yet. Computing classifier now")

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
            clf = LogisticRegression()
        elif classification_method == "gradient_boosting":
            clf = GradientBoostingClassifier(n_estimators=100)
        
        else:
            raise ValueError(
                f"Invalid classification method: {classification_method}")


        clf = clf.fit(x_train, y_train)

        store_cache_variable(clf,classifier_filepath)

    return clf


#TODO: tailor this again to backend
def classification(log_path, classification_method,measure_name,ready_training):
    if classification_method == "autofolio":
        return autofolio_classification(log_path,measure_name)
 


    clf = read_fitted_classifier(classification_method,measure_name,ready_training)

    predictions = clf.predict(read_feature_vector(log_path))


    return predictions[0] 

def ranking_classification(log_path, classification_method,measure_name):
    if classification_method == "autofolio":
        return autofolio_classification(log_path,measure_name)
 

    clf = read_fitted_classifier(classification_method,measure_name,[])

    # Get probability estimates for each class
    proba = clf.predict_proba(read_feature_vector(log_path))

    # Assuming you want to get the rankings for each instance in X_test
    # argsort gives the indices that would sort an array in ascending order

    class_labels = clf.classes_

    ranking = np.argsort(-proba, axis=1)

    sorted_class_names = class_labels[ranking]

    class_ranking_array = [sorted_class_names[:, i][0] for i in range(sorted_class_names.shape[1])]

    for algo in globals.algorithm_portfolio:
        if algo not in class_ranking_array:
            class_ranking_array += [algo]
    return class_ranking_array



def final_prediction(log_path, measure_weight):
    """returns the predicted rankings
    1st place ILP => ret["ILP"] = 1
    Args:
        log_path: _description_
        measure_weight: _description_

    Returns:
        _description_
    """
    max_measure = max(measure_weight, key=lambda k: measure_weight[k])
    class_ranking_array = ranking_classification(log_path,"gradient_boosting",max_measure)
    ret = {}
    i = 1
    for class_label in class_ranking_array:
        ret[class_label] = i
        i+=1
    return ret
    


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

def list_files_with_sizes(file_paths):
    # Create a list to store file details
    file_details = []

    # Iterate over each file path
    for file_path in file_paths:
        # Get file size in bytes
        file_size = os.path.getsize(file_path)

        # Append file details to the list
        file_details.append((file_path, file_size))

    # Sort the list based on file size in descending order
    file_details.sort(key=lambda x: x[1], reverse=True)

    # Print the sorted file details
    for file_path, file_size in file_details:
        print(f"{file_path}: {file_size} bytes")

if __name__ == "__main__":

    log_paths = gather_all_xes("../logs/real_life_logs")


    list_files_with_sizes(log_paths)

    input("done")

    param_grid = {
    'n_estimators': [50, 100, 200,400,800],
    'learning_rate': [0.01, 0.1, 0.2,0.3,0.4],
    'max_depth': [3, 5, 7,9,12],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4,6]
    }

    init()
    ready_training = get_all_ready_logs_multiple(gather_all_xes("../logs/training"))
    ready_testing  = get_all_ready_logs_multiple(gather_all_xes("../logs/testing"))


    x_train = read_feature_matrix(ready_training)
    y_train =  read_target_vector(ready_training,"runtime")

    x_test = read_feature_matrix(ready_testing)
    y_test =  read_target_vector(ready_testing,"runtime")

    gb_clf = GradientBoostingClassifier()

    grid_search = GridSearchCV(gb_clf, param_grid, cv=5, n_jobs=-1)
    grid_search.fit(x_train, y_train)

    # Get the best hyperparameters
    best_params = grid_search.best_params_
    print("Best Hyperparameters:", best_params)


    # Train the model with the best hyperparameters
    best_gb_clf = GradientBoostingClassifier(**best_params)
    best_gb_clf.fit(x_train, y_train)

# Evaluate the model
    accuracy = best_gb_clf.score(x_test, y_test)
    print("Accuracy on Test Set:", accuracy)

    input("done")


