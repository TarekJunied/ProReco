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
from measures import read_measure_entry,read_regression_target_vector
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
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor





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

        y_train = read_classification_target_vector(ready_training, measure_name)

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


def read_fitted_regressor(regression_method, measure_name,discovery_algorithm, ready_training):
    regressor_filepath = f"./regressors/{regression_method}/{discovery_algorithm}_{measure_name}.pkl"
    
    try:
        reg = load_cache_variable(regressor_filepath)
    except Exception:
        print("Regressor doesn't exist yet. Computing regressor now")

        x_train = read_feature_matrix(ready_training)
        y_train = read_regression_target_vector(ready_training, discovery_algorithm,measure_name)

        if regression_method == "linear_regression":
            reg = LinearRegression()
        elif regression_method == "ridge_regression":
            reg = Ridge(alpha=1.0)
        elif regression_method == "lasso_regression":
            reg = Lasso(alpha=1.0)
        elif regression_method == "decision_tree":
            reg = DecisionTreeRegressor()
        elif regression_method == "random_forest":
            reg = RandomForestRegressor()
        elif regression_method == "gradient_boosting":
            reg = GradientBoostingRegressor(n_estimators=100)
        elif regression_method == "svm":
            reg = SVR()
        elif regression_method == "knn":
            reg = KNeighborsRegressor(n_neighbors=5)
        elif regression_method == "mlp":
            reg = MLPRegressor(hidden_layer_sizes=(100,), max_iter=500)
        else:
            raise ValueError(f"Invalid regression method: {regression_method}")

        reg = reg.fit(x_train, y_train)
        store_cache_variable(reg, regressor_filepath)

    return reg




#TODO: tailor this again to backend
def classification(log_path, classification_method,measure_name,ready_training):
    if classification_method == "autofolio":
        return autofolio_classification(log_path,measure_name)


    clf = read_fitted_classifier(classification_method,measure_name,ready_training)

    predictions = clf.predict(read_feature_vector(log_path))

    return predictions[0] 

#TODO: tailor this again to backend
def regression(log_path, regression_method, measure_name, discovery_algorithm, ready_training):
 
    reg = read_fitted_regressor(regression_method, measure_name,discovery_algorithm, ready_training)

    prediction = reg.predict(read_feature_vector(log_path))

    return prediction[0]


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


def predict_regression(log_path, measure_name,regression_method="linear_regression"):
    predicted_values = {}
    ready_training = list(globals.training_log_paths.keys())
    for discovery_algorithm in globals.algorithm_portfolio:
        predicted_values[discovery_algorithm] = regression(log_path,regression_method,measure_name,discovery_algorithm,ready_training)

    if globals.measures_kind[measure_name] =="max":
        ret = max(predicted_values, key=predicted_values.get)
    elif globals.measures_kind[measure_name] =="min":
        ret = min(predicted_values, key=predicted_values.get)
    else:
        print("Invalid kind of measures")
        input(measure_name)

        ret = None
    return ret



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

    #init()
    log_paths = get_all_ready_logs_multiple(gather_all_xes("../logs/training"))
    input(len(log_paths))





    input("stop")
    ready_training = get_all_ready_logs_multiple(gather_all_xes("../logs/training"))
    log_path = ready_training[0]
    for regression_method in globals.regression_methods:
        for measure_name in globals.measures_list:
            for discovery_algorithm in globals.algorithm_portfolio:
                print(regression(log_path,regression_method,measure_name,discovery_algorithm,ready_training))

    

