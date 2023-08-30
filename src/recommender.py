import pm4py
import os
import numpy as np
import globals
from filehelper import gather_all_xes, select_smallest_k_logs
from sklearn.neighbors import KNeighborsClassifier
from features import compute_features_of_log, init_feature_matrix
from measures import init_target_vector, init_target_entry
from utils import read_logs, compute_models, pickle_retrieve, pickle_dump, load_all_globals_from_cache, load_target_vector_into_y


def init():
    globals.training_logs_paths = gather_all_xes("./LogGenerator/logs")
    globals.training_logs_paths = select_smallest_k_logs(
        20, "./LogGenerator/Logs")
    if os.path.getsize(globals.cache_file) == 0:
        read_logs()
        print("Now finished reading logs")
        print(globals.training_logs_paths)
        print(globals.logs)
        compute_models()
        print("Now finished computing models and runtime")
        init_feature_matrix()
        print("Now finished computing feature matrix")

        init_target_vector(globals.selected_measure)
        print("now finished computing target_vector")
        print(globals.y)
        pickle_dump()

    else:
        pickle_retrieve()
        load_all_globals_from_cache()
        print("Now we retrieved everything from cache, let's check if everything was cached properly")

        print("Now finished reading logs")
        print(globals.training_logs_paths)

        print("Now finished computing models and runtime")

        print("Now finished computing feature matrix")

        load_target_vector_into_y()
        print("now finished computing target_vector")
        print(globals.y)


def classification(new_log_path):
    knn = KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto',
                               p=2, metric="minkowski")
    knn.fit(globals.X, globals.y)

    prediction = knn.predict(compute_features_of_log(new_log_path))

    globals.predictions[new_log_path] = prediction

    print("predicition is ", prediction)

    return prediction


init()
correct = 0
n = len(globals.training_logs_paths)
for i in range(n):
    log_path = globals.training_logs_paths[i]
    init_target_entry(
        log_path, i, globals.selected_measure)
    prediction = classification(log_path)

    if globals.target_vectors[log_path, globals.selected_measure] == prediction:
        correct += 1

print(correct)
print(n)
print(correct/n)
