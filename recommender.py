import pm4py
from filehelper import gather_all_xes, select_smallest_k_logs
import os
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from globals import  logs,  selected_measure,models,cache_file,target_vectors,X
from features import (
    compute_features_of_log,
    init_feature_matrix
)
from measures import (
    init_target_vector
)
from utils import read_logs, compute_models, pickle_retrieve, pickle_dump,load_all_globals_from_cache



def init():
    global y, X, training_logs_paths
    training_logs_paths = select_smallest_k_logs(3)
    if os.path.getsize(cache_file) == 0:
        read_logs()
        print("Now finished reading logs")
        print(training_logs_paths)
        print(logs)
        compute_models()
        print("Now finished computing models and runtime")
        print(models)
        init_feature_matrix()
        print("Now finished computing feature matrix")
        print(np.array2string(X, separator=', ', formatter={
            'all': lambda x: f'{x:.2f}'}, suppress_small=True))
        init_target_vector(selected_measure)
        print("now finished computing target_vector")
        print(y)
        pickle_dump()

    else:
        pickle_retrieve()
        load_all_globals_from_cache()
        print("Now we retrieved everything from cache, let's check if everything was cached properly")

        print("Now finished reading logs")
        print(training_logs_paths)
        print(logs)

        print("Now finished computing models and runtime")
        print(models)

        print("Now finished computing feature matrix")
        print(np.array2string(X, separator=', ', formatter={
        'all': lambda x: f'{x:.2f}'}, suppress_small=True))

        if (training_logs_paths[0], selected_measure) not in target_vectors:
            init_target_vector(selected_measure)
        else:
            for i in range(len(training_logs_paths)):
                y[i] = target_vectors[training_logs_paths[i], selected_measure]

        print("now finished computing target_vector")
        print(y)





def classification(new_log_path):
    knn = KNeighborsClassifier(n_neighbors=1, weights='uniform', algorithm='auto',
                               p=2, metric="minkowski")
    knn.fit(X, y)

    prediction = knn.predict(compute_features_of_log(new_log_path))

    print("predicition is ", prediction)

    return prediction

init()