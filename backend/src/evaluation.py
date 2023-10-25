import sys
import matplotlib.pyplot as plt
import numpy as np
import time
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import numpy as np
import globals
from utils import get_all_ready_logs,load_cache_variable
from recommender import classification
from filehelper import gather_all_xes, select_smallest_k_logs,split_file_path
from measures import read_target_entries, read_target_entry, read_target_vector,  read_worst_entry
from features import read_feature_matrix

def get_number_one(input_dict):
    for key, value in input_dict.items():
        if value == 1:
            return key
    return None  # Return None if no key with value 1 is found



def create_evaluation_plot(training_log_paths, testing_log_paths, selected_measures, classification_method="knn"):
    values = []
    categories = selected_measures
    display_str = ""
    for measure in selected_measures:
            
        
        ready_testing = get_all_ready_logs(testing_log_paths,measure)
        ready_training = get_all_ready_logs(training_log_paths,measure)

        display_str += f" {len(ready_testing)} "
        values += [evaluate_measure_accuracy(ready_training,ready_testing,measure,classification_method)]


    plt.figure(figsize=(8, 6))  # Adjust the figure size if needed
    plt.bar(categories, values, color='royalblue')
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title(display_str)
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)  # Add a horizontal grid
    plt.xticks(rotation=90)
    
    plt.savefig(f'../evaluation/{classification_method}_accuracy_{int(time.time())}.png', dpi=300, bbox_inches='tight')







def evaluate_measure_accuracy(training_log_paths, testing_log_paths, measure_name, classification_method="knn"):

    if measure_name not in globals.normalisierbare_measures:
        print("Can't evaluate accuracy for this measure")
        return False

    
    y_best = [None]*(len(testing_log_paths))
    y_worst = [None]*(len(testing_log_paths))
    y_pred = [None]*(len(testing_log_paths))

    x_train = read_feature_matrix(training_log_paths)

    training_log_paths = get_all_ready_logs(training_log_paths, measure_name)
    y_train = read_target_vector(training_log_paths, measure_name)

  

    print(f"We have {len(training_log_paths)} training logs")
    print(f"We have {len(testing_log_paths)} testing logs")

    sum = 0

    for i in range(len(testing_log_paths)):

        y_best[i] = read_target_entry(
            testing_log_paths[i], measure_name)
        y_worst[i] =  read_worst_entry(testing_log_paths[i], measure_name)
        y_pred[i] = get_number_one(classification(
            testing_log_paths[i], x_train, y_train, classification_method)[1])

        cur_name_log = split_file_path(testing_log_paths[i])["filename"]

        cur_max_val = load_cache_variable(f"./cache/measures/{y_best[i]}_{measure_name}_{cur_name_log}.pkl")
        cur_min_val = load_cache_variable(f"./cache/measures/{y_worst[i]}_{measure_name}_{cur_name_log}.pkl")
        if y_best[i] == y_worst[i]:
            print("wtf")
        cur_pred_val = load_cache_variable(f"./cache/measures/{y_pred[i]}_{measure_name}_{cur_name_log}.pkl")

        if cur_max_val == cur_min_val:
            cur_min_max = 1
        else:
            cur_min_max = (cur_pred_val - cur_min_val) / (cur_max_val - cur_min_val)


        sum += cur_min_max
      
    return sum / len(testing_log_paths)


if __name__ == "__main__":
    sys.setrecursionlimit(5000)

    selected_measures = ['token_fitness', 'alignment_fitness', 'token_precision', 'alignment_precision','generalization', 'pm4py_simplicity']



    testing_logpaths = gather_all_xes("../logs/testing/")
    training_logpaths = gather_all_xes("../logs/training/")



    for classification_method in globals.classification_methods:
        create_evaluation_plot(training_logpaths, testing_logpaths, selected_measures,classification_method=classification_method)




    input("stop")

    selected_measures = globals.measures

    for measure_name in selected_measures:
        ready_for_testingpaths = get_all_ready_logs(
        testing_logpaths,measure_name)
        ready_for_trainingpaths = get_all_ready_logs(
        training_logppaths, measure_name)


        evaluate_measure_accuracy(ready_for_trainingpaths,
                                  ready_for_testingpaths, measure_name, "knn")
