import pm4py
from utils import read_log
from globals import selected_features, log_paths
import numpy as np

def init_causal_matrix(matrix, activities):
    for a in activities:
        for b in activities:
            matrix[a,b] = 0


def feature_causality_strength(log_path):
    activities = get_all_activities_of_log(log_path)
    matrix = causal_matrix(log_path)
    cur_max = float("-Inf")

    for i in range(len(activities)):
        for j in range(i+1, len(activities)):
            if abs(matrix[activities[i],activities[j]]) > cur_max:
                cur_max = abs(matrix[activities[i],activities[j]])

    return cur_max

def causal_transform_diagonal_entries(matrix,activities):
    for a in activities:
        v = matrix[a,a]
        matrix[a,a] = v / (v+1)

def causal_transform_nondiagonal_entries(matrix,activities):
    list_activities = list(activities)
    for i in range(0,len(list_activities)):
        for j in range(i+1, len(list_activities)):
            a = list_activities[i]
            b = list_activities[j]
            a_b = matrix[a,b]
            b_a = matrix[b,a]
            matrix[a,b] = (a_b - b_a) / (a_b + b_a + 1)
            matrix[b,a] = -matrix[a,b]


def causal_matrix(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list(variants.keys())

    activities = get_all_activities_of_log(log_path)
    matrix = {}

    init_causal_matrix(matrix,activities)

    # do the counting
    for trace in trace_variants:
        for i in range(0,len(trace)-1):
            matrix[trace[i],trace[i+1]] += variants[trace]


    causal_transform_diagonal_entries(matrix,activities)


    causal_transform_nondiagonal_entries(matrix,activities)


    return matrix




def get_all_activities_of_log(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list(variants.keys())
    activities = set()

    for trace in trace_variants:
        for i in range(0, len(trace)):
            activity = trace[i]
            if activity not in activities:
                activities.add(activity)
    return list(activities)



def feature_no_distinct_start(log_path):
    log = read_log(log_path)
    return len(pm4py.get_start_activities(log))


def feature_no_distinct_end(log_path):
    log = read_log(log_path)
    return len(pm4py.get_end_activities(log))


def feature_no_events_total(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list(variants.keys())

    sum = 0
    for trace in trace_variants:
        sum += variants[trace] * len(trace)

    return sum


def feature_no_distinct_events(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list(variants.keys())
    activities = set()

    for trace in trace_variants:
        for i in range(0, len(trace)):
            activity = trace[i]
            if activity not in activities:
                activities.add(activity)
    return len(activities)


def feature_avg_event_repetition_intra_trace(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list(variants.keys())
    event_repetitions = 0

    for trace in trace_variants:
        seen_activities = set()
        for i in range(0, len(trace)):
            cur_activity = trace[i]
            if cur_activity not in seen_activities:
                seen_activities.add(trace[i])
            else:
                event_repetitions += variants[trace]
    return event_repetitions / feature_no_total_traces(log_path)


def feature_no_distinct_traces(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list(variants.keys())

    return len(trace_variants)


def feature_no_total_traces(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list(variants.keys())

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

def feature_density(log_path):
    activities = get_all_activities_of_log(log_path)
    n = len(activities)
    matrix = causal_matrix(log_path)

    non_zero_count = 0

    for a in activities:
        for b in activities:
            if matrix[a,b] != 0:
                non_zero_count +=1

    return non_zero_count / (n**2)


def feature_length_one_loops(log_path):
    activities = get_all_activities_of_log(log_path)
    n = len(activities)
    matrix = causal_matrix(log_path)

    counter = 0
    for a in activities:
        if matrix[a,a] > 0:
            counter += 1

    return counter/ n



def compute_features_of_log(log_path):
    X_test = np.empty((1, len(selected_features)))
    for feature_index in range(len(selected_features)):
        X_test[0, feature_index] = compute_feature_log_path(log_path, feature_index)

    print(X_test)
    return X_test


def compute_feature_log_path(log_path, feature_index):
    if selected_features[feature_index] == "no_distinct_traces":
        ret = feature_no_distinct_traces(log_path)
    elif selected_features[feature_index] == "no_total_traces":
        ret = feature_no_total_traces(log_path)
    elif selected_features[feature_index] == "avg_trace_length":
        ret = feature_avg_trace_length(log_path)
    elif selected_features[feature_index] == "avg_event_repetition_intra_trace":
        ret = feature_avg_event_repetition_intra_trace(log_path)
    elif selected_features[feature_index] == "no_distinct_events":
        ret = feature_no_distinct_events(log_path)
    elif selected_features[feature_index] == "no_events_total":
        ret = feature_no_events_total(log_path)
    elif selected_features[feature_index] == "no_distinct_start":
        ret = feature_no_distinct_start(log_path)
    elif selected_features[feature_index] == "no_distinct_end":
        ret = feature_no_distinct_end(log_path)
    elif selected_features[feature_index] == "causality_strength":
        ret = feature_causality_strength(log_path)
    elif selected_features[feature_index] == "density":
        ret = feature_density(log_path)
    elif selected_features[feature_index] == "length_one_loops":
        ret = feature_length_one_loops(log_path)
    else:
        ret = None
        print("Invalid feature name")
    return ret


def compute_feature(log_index, feature_index):
    log_path = log_paths[log_index]
    return compute_feature_log_path(log_path,feature_index)