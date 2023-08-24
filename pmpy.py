import pm4py
import sklearn
from filehelper import *
import numpy as np

algorithm_portfolio = ["alpha","heuristic","ILP","inductive"]
features_list = ["no_distinct_traces","no_total_traces","avg_trace_length","avg_event_repetition_intra_trace","no_distinct_events"
                 ,"no_events_total","no_distinct_start","no_distinct_end","entropy","concurrency","density","length-one-loops"]

selected_features =  ["no_distinct_traces","no_total_traces","avg_trace_length","no_distinct_events"
                 ,"no_events_total","no_distinct_start","no_distinct_end"]

models = {}
log_paths = []
logs = {}

def load_all_logs():
    log_paths = gather_all_xes("./")
    for log_path in log_paths:
        read_log(log_path)

def compute_all_models():
    for discovery_algorithm in algorithm_portfolio:
        for log_path in log_paths:
            read_model(log_path,discovery_algorithm)

def compute_feature(log_index, feature_index):


def init_feature_matrix():
    X = np.empty((len(log_paths), len(selected_features)))
    for i in range(len(log_paths)):
        for j in range(len(selected_features)):
            X[i,j] = compute_feature(log_index, feature_index)




def init():
    load_all_logs()
    compute_all_models()
    init_feature_matrix()





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

def classification(new_log_path):
    sklearn.neighbors.KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto', 
                                            p=2, metric="minkowski")




init()
