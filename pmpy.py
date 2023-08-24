import pm4py
import sklearn
from filehelper import *
import numpy as np
import pickle
from sklearn.neighbors import KNeighborsClassifier


algorithm_portfolio = ["alpha","heuristic","inductive"]
features_list = ["no_distinct_traces","no_total_traces","avg_trace_length","avg_event_repetition_intra_trace","no_distinct_events"
                 ,"no_events_total","no_distinct_start","no_distinct_end","entropy","concurrency","density","length-one-loops"]

selected_features =  ["no_distinct_traces","no_total_traces","avg_trace_length","no_distinct_events"
                 ,"no_events_total","no_distinct_start","no_distinct_end"]

models = {}
log_paths = []
logs = {}
cached_variables = {}
y = None

X = None


def load_all_logs_into_cache():
    global log_paths
    log_paths = gather_all_xes("./")[:4]
    y = [None] * len(log_paths)
    for i in range(0,5):
        read_log(log_paths[i])

    cached_variables["logs"] = logs
    cached_variables["log_paths"] = log_paths

    with open("cache.pkl", "wb") as file:
        pickle.dump(cached_variables, file)

def load_all_logs_from_cache():
    global cached_variables, log_paths, logs
    log_paths = gather_all_xes("./")[:4]
    if os.path.getsize("cache.pkl") == 0:
        load_all_logs_into_cache()
    else:
        with open("cache.pkl", "rb") as file:
            cached_variables = pickle.load(file)
        log_paths = cached_variables["log_paths"]
        logs = cached_variables["logs"]


def compute_all_models():
    for discovery_algorithm in algorithm_portfolio:
        for log_path in log_paths:
            read_model(log_path,discovery_algorithm)


def compute_feature(log_index, feature_index):
    log_path = log_paths[log_index]
    if selected_features[feature_index] == "no_distinct_traces":
        ret = feature_no_distinct_traces(log_path)
    elif selected_features[feature_index] == "no_total_traces":
        ret = feature_no_total_traces(log_path)
    elif selected_features[feature_index] == "avg_trace_length":
        ret = feature_avg_trace_length(log_path)
    elif selected_features[feature_index] == "no_distinct_events":
        ret = feature_no_distinct_events(log_path)
    elif selected_features[feature_index] == "no_events_total":
        ret = feature_no_events_total(log_path)
    elif selected_features[feature_index] == "no_distinct_start":
        ret = feature_no_distinct_start(log_path)
    elif selected_features[feature_index] == "no_distinct_end":
        ret = feature_no_distinct_end(log_path)
    else:
        ret = None
        print("Invalid feature name")
    return ret


def init_feature_matrix():
    global X, cached_variables
    X = np.empty((len(log_paths), len(selected_features)))
    for log_index in range(len(log_paths)):
        for feature_index in range(len(selected_features)):
            X[log_index,feature_index] = compute_feature(log_index, feature_index)

def init_target(log_path,log_index):
    global y
    cur_fit = float("-inf")
    for discovery_algorithm in algorithm_portfolio:
        algo_fit = fitness_token_based_replay(log_path,discovery_algorithm)
        if( algo_fit > cur_fit):
            cur_fit = algo_fit
            y[log_index] = discovery_algorithm



def select_smallest_k_logs(k):
        # Create a list of tuples containing (file_path, file_size)
        files_with_sizes = [(file_path, os.path.getsize(file_path)) for file_path in log_paths]

        # Sort the list of tuples by file size
        sorted_files = sorted(files_with_sizes, key=lambda x: x[1])

        # Extract the sorted file paths from the sorted list of tuples
        sorted_file_paths = [file_path for file_path, _ in sorted_files]

        return sorted_file_paths[:k]

def init():
    global y, X,log_paths
    load_all_logs_from_cache()

    log_paths = select_smallest_k_logs(2)

    X = np.empty((len(log_paths), len(selected_features)))
    y = [None] * len(log_paths)

    print("now finished loading all logs from cache")
    
    init_feature_matrix()
    print("now finished initializing feature matrix")
    # determine the best algorithm for all logs
    for i in range(len(log_paths)):
        init_target(log_paths[i], i)

    print("now finished initializing target vector")

    matrix_string = np.array2string(X, separator=', ', formatter={'all': lambda x: f'{x:.2f}'}, suppress_small=True)
    print("now printing feature matrix")
    print(matrix_string)
    print("now printing y:")
    print(y)






def print_distinct_traces(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list(variants.keys())

    for trace in trace_variants:
        print(trace)

def read_model(log_path, discovery_algorithm):
    if (log_path,discovery_algorithm) not in models:
        log = read_log(log_path)
        if discovery_algorithm  == "alpha":
            net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(log) 
            models[log_path,discovery_algorithm] = (net,initial_marking,final_marking)

        elif discovery_algorithm == "heuristic":
            net, initial_marking, final_marking = pm4py.discover_petri_net_heuristics(log) 
            models[log_path,discovery_algorithm] = (net,initial_marking,final_marking)
        elif discovery_algorithm == "ILP":
            net, initial_marking, final_marking = pm4py.discover_petri_net_ilp(log) 
            models[log_path,discovery_algorithm] = (net,initial_marking,final_marking)

        elif discovery_algorithm == "inductive":
            net,initial_marking,final_marking = pm4py.discover_petri_net_inductive(log)
            models[log_path,discovery_algorithm] = (net,initial_marking,final_marking)

    return models[log_path,discovery_algorithm]




def read_log(log_path):
    if log_path in logs:
        return logs[log_path]
    else:
        try:
            log = pm4py.read_xes(log_path)
            logs[log_path] = log
            return log
        except Exception:
            print("The log does not exist !")

def get_all_activities_of_log(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list(variants.keys())
    activities = set()

    for trace in trace_variants:
        for i in range(0,len(trace)):
            activity = trace[i]
            if activity not in activities:
                activities.add(activity)
    return list(activities)
def feature_concurrency(log_path):
    log = read_log(log_path)
    footprints = pm4py.discover_footprints(log, case_id_key='case:concept:name', timestamp_key='time:timestamp')
    print(footprints)
   


def feature_no_distinct_start(log_path):
    log = read_log(log_path)
    return len(pm4py.get_start_activities(log))

def feature_no_distinct_end(log_path):
    log = read_log(log_path)
    return len(pm4py.get_end_activities(log))


def feature_no_events_total(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list( variants.keys())

    sum = 0
    for trace in trace_variants:
        sum += variants[trace]*len(trace)

    return sum

def feature_no_distinct_events(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list(variants.keys())
    activities = set()

    for trace in trace_variants:
        for i in range(0,len(trace)):
            activity = trace[i]
            if activity not in activities:
                activities.add(activity)
    return len(activities)


def feature_avg_event_repetition_intra_trace(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list( variants.keys())
    activities = {}

    for trace in trace_variants:
        for i in range(0,len(trace)):
            activity = trace[i]
            if activity not in activities:
                activities[activity] += variants[trace]
    return "I don't know yet"


def feature_no_distinct_traces(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list( variants.keys())
    
    return len(trace_variants)

def feature_no_total_traces(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list( variants.keys())

    sum = 0
    for trace in trace_variants:
        sum += variants[trace]

    return sum

def feature_avg_trace_length(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list(variants.keys())

    sum_of_all_trace_lengths = 0
    for trace in trace_variants:
        sum_of_all_trace_lengths += len(trace)

    return sum_of_all_trace_lengths / feature_no_total_traces(log_path)







def compute_features_from_log(log_path,feature_name):
    if feature_name == "no_distinct_traces":
        log = read_log(log_path)
        variants = pm4py.stats.get_variants(log)
        trace_variants = variants.keys()
        sum = 0
        for trace in trace_variants:
            sum += variants[trace]
        print(sum)

def compute_feature_log_path(log_path, feature_index):
    if selected_features[feature_index] == "no_distinct_traces":
        ret = feature_no_distinct_traces(log_path)
    elif selected_features[feature_index] == "no_total_traces":
        ret = feature_no_total_traces(log_path)
    elif selected_features[feature_index] == "avg_trace_length":
        ret = feature_avg_trace_length(log_path)
    elif selected_features[feature_index] == "no_distinct_events":
        ret = feature_no_distinct_events(log_path)
    elif selected_features[feature_index] == "no_events_total":
        ret = feature_no_events_total(log_path)
    elif selected_features[feature_index] == "no_distinct_start":
        ret = feature_no_distinct_start(log_path)
    elif selected_features[feature_index] == "no_distinct_end":
        ret = feature_no_distinct_end(log_path)
    else:
        ret = None
        print("Invalid feature name")
    return ret


def compute_features_of_log(log_path):
    X_test = np.empty((1, len(selected_features)))
    for feature_index in range(len(selected_features)):
        X_test[0,feature_index] = compute_feature_log_path(log_path, feature_index)
    return X_test



def classification(new_log_path):

    knn = KNeighborsClassifier(n_neighbors=1, weights='uniform', algorithm='auto',
                                            p=2, metric="minkowski")
    knn.fit(X ,y)


    prediction = knn.predict(compute_features_of_log(new_log_path))

    print("prediciton is ", prediction)

    return prediction



def fitness_token_based_replay(log_path,discovery_algorithm):
    log = read_log(log_path)
    petri_net,initial_marking,final_marking = read_model(log_path,discovery_algorithm)
    result = pm4py.conformance.fitness_token_based_replay(log, petri_net,initial_marking, final_marking)
    print(discovery_algorithm, result["average_trace_fitness"])
    return result["average_trace_fitness"]


init()
classification(log_paths[0])




