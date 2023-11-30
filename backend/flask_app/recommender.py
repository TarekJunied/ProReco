import multiprocessing
import globals
import numpy as np
import subprocess
import os
import re
import pm4py
import sys
from utils import read_logs, read_models,  get_all_ready_logs, read_log, split_data
from filehelper import gather_all_xes, get_all_ready_logs, get_all_ready_logs_multiple
from features import read_feature_matrix, read_feature_vector, feature_no_total_traces,space_out_feature_vector_string
from measures import read_target_entry, read_target_entries, read_measure_entry
from init import *
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.impute import SimpleImputer
from autofolio_interface import create_performance_csv,create_feature_csv
import sklearn


label_to_index = {label: index for index,
                  label in enumerate(globals.algorithm_portfolio)}


all_labels = list(label_to_index.keys())
def activate_smac_env():
    subprocess.run("conda run -n SMAC",shell=True)


def extract_prediction_from_autofolio_string(autofolio_string):
    # Define a regular expression pattern to capture the word after "('inductive',"
    pattern = r"\('(\w+)',"

    # Use re.search to find the first match
    match = re.search(pattern, autofolio_string)

    # Check if a match is found
    if match:
        # Extract and return the captured word
        return match.group(1)
    else:
        # Return None if no match is found
        return "AutoFolio Error"

def read_autofolio_predictor(training_logpaths,testing_logpaths,measure_name):
    if os.path.exists(f"./AutoFolio/af_predictors/{measure_name}_predictor.af"):
        ret = f"./af_predictors/{measure_name}_predictor.af"
    else:
        ret = f"./{create_autofolio_predictor(training_logpaths,testing_logpaths,measure_name)}"
    return ret







def create_autofolio_predictor(training_logpaths,testing_logpaths,measure_name):



    training_features_filename = f"{measure_name}_training_features.csv"
    training_performance_filename =f"{measure_name}_training_performance.csv"
    testing_features_filename = f"{measure_name}_testing_features.csv"
    testing_performance_filename =f"{measure_name}_testing_performance.csv"



    training_features_filepath = f"./AutoFolio/csv_files/{measure_name}_training_features.csv"
    training_performance_filepath =f"./AutoFolio/csv_files/{measure_name}_training_performance.csv"
    testing_features_filepath = f"./AutoFolio/csv_files/{measure_name}_testing_features.csv"
    testing_performance_filepath =f"./AutoFolio/csv_files/{measure_name}_testing_performance.csv"


    create_feature_csv(training_logpaths,training_features_filepath)
    create_performance_csv(training_logpaths,measure_name,training_performance_filepath)

    create_feature_csv(testing_logpaths,testing_features_filepath)
    create_performance_csv(testing_logpaths,measure_name,testing_performance_filepath)

    predictor_filepath = f"./af_predictors/{measure_name}_predictor.af"

    if globals.measures_kind[measure_name] == "max": 
        max_string = "--maximize"
    elif globals.measures_kind[measure_name] == "min":
        max_string = ""
    else:
        print("invalid kind of measure")
        sys.exit(-1)


    if measure_name == "runtime" or measure_name =="log_runtime":
        objective_string = "runtime"
    else:
        objective_string = "solution_quality"
    objective_string="solution_quality"

    command = [
    "python",
    f"./scripts/autofolio",
    "--performance_csv", f"./csv_files/{training_performance_filename}",
    "--feature_csv",  f"./csv_files/{training_features_filename}",
    "--objective ", objective_string,
    "--tune",
    max_string,
    "--save", predictor_filepath,

    ]

    command_str = " ".join(command)



    os.chdir(os.path.abspath("./AutoFolio"))

    subprocess.run(command_str,shell=True)


    os.chdir("../")
    return predictor_filepath


def autofolio_classification(log_path,measure_name):

    

    training_logpaths = list(globals.training_log_paths.keys())
    testing_logpaths = list(globals.testing_log_paths.keys())

    predictor_filepath = read_autofolio_predictor(training_logpaths,testing_logpaths,measure_name)


    spaced_out_feature_vector_string = space_out_feature_vector_string(log_path)

    command=[
        "python",
        "scripts/autofolio",
        "--load",
        predictor_filepath,
        "--feature_vec",
        spaced_out_feature_vector_string]


    os.chdir("./AutoFolio")


    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
        print("Command output:")
        print(output)
    except subprocess.CalledProcessError as e:
        print("Error executing command. Return code:", e.returncode)
        print("Command output (if any):")
        print(e.output)
   
    prediction = extract_prediction_from_autofolio_string(output)

    if prediction not in globals.algorithm_portfolio:
        input("an error occureed with autofolio")
        return 
    
    os.chdir("../")

    return prediction



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


if __name__ == "__main__":


    input(len(gather_all_xes("../logs/real_life_logs")))


