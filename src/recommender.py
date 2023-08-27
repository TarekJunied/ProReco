import pm4py
from filehelper import gather_all_xes, select_smallest_k_logs
import os
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import globals
from features import (
    compute_features_of_log,
    init_feature_matrix
)
from measures import (
    init_target_vector
)
from utils import read_logs, compute_models, pickle_retrieve, pickle_dump, load_all_globals_from_cache


def init():
    globals.training_logs_paths = gather_all_xes("../logs")
    if os.path.getsize(globals.cache_file) == 0:
        read_logs()
        print("Now finished reading logs")
        print(globals.training_logs_paths)
        print(globals.logs)
        compute_models()
        print("Now finished computing models and runtime")
        print(globals.models)
        init_feature_matrix()
        print("Now finished computing feature matrix")
        print(np.array2string(globals.X, separator=', ', formatter={
            'all': lambda x: f'{x:.2f}'}, suppress_small=True))
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
        print(globals.logs)

        print("Now finished computing models and runtime")
        print(globals.models)

        print("Now finished computing feature matrix")
        print(np.array2string(globals.X, separator=', ', formatter={
            'all': lambda x: f'{x:.2f}'}, suppress_small=True))

        globals.y = [None] * len(globals.training_logs_paths)
        if (globals.training_logs_paths[0], globals.selected_measure) not in globals.target_vectors:

            init_target_vector(globals.selected_measure)
        else:
            for i in range(len(globals.training_logs_paths)):
                globals.y[i] = globals.target_vectors[globals.training_logs_paths[i],
                                                      globals.selected_measure]

        print("now finished computing target_vector")
        print(globals.y)


def classification(new_log_path):
    knn = KNeighborsClassifier(n_neighbors=1, weights='uniform', algorithm='auto',
                               p=2, metric="minkowski")
    knn.fit(globals.X, globals.y)

    prediction = knn.predict(compute_features_of_log(new_log_path))

    print("predicition is ", prediction)

    return prediction


init()
