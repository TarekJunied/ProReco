import pm4py
import time
import os
import globals
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from utils import read_log, generate_log_id, generate_cache_file, store_cache_variable, load_cache_variable, get_log_name
from filehelper import gather_all_xes,split_file_path
from pm4py.algo.discovery.footprints import algorithm as footprints_discovery
from scipy.stats import variation, entropy




def create_networkx_graph_from_dfg(log_path):
    log = read_log(log_path)
    dfg,start_activities,end_activities =  pm4py.discover_dfg(log)

    G = nx.DiGraph()

    artificial_start_node = "artificial_start"
    G.add_node(artificial_start_node)
    for start_activity in start_activities:
        G.add_edge(artificial_start_node, start_activity, weight=0)  

    artificial_end_node = "artificial_end"
    G.add_node(artificial_end_node)
    for end_activity in end_activities:
        G.add_edge(end_activity, artificial_end_node, weight=0)  


    for edge in dfg:
        G.add_edge(edge[0],edge[1],weight=dfg[edge])

    return G


def read_networkx_graph_of_log(log_path):
    log_name = get_log_name(log_path)
    try:
        G = load_cache_variable(f"./cache/models/dfg_{log_name}.pkl")
    except Exception:
        G = create_networkx_graph_from_dfg(log_path)
        store_cache_variable(G,f"./cache/models/dfg_{log_name}.pkl")
    return G

def init_causal_matrix(matrix, activities):
    for a in activities:
        for b in activities:
            matrix[a, b] = 0



def causal_transform_diagonal_entries(matrix, activities):
    for a in activities:
        v = matrix[a, a]
        matrix[a, a] = v / (v+1)


def causal_transform_nondiagonal_entries(matrix, activities):
    list_activities = list(activities)
    for i in range(0, len(list_activities)):
        for j in range(i+1, len(list_activities)):
            a = list_activities[i]
            b = list_activities[j]
            a_b = matrix[a, b]
            b_a = matrix[b, a]
            matrix[a, b] = (a_b - b_a) / (a_b + b_a + 1)
            matrix[b, a] = -matrix[a, b]


def causal_matrix(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list(variants.keys())

    activities = get_all_activities_of_log(log_path)
    matrix = {}

    init_causal_matrix(matrix, activities)

    # do the counting
    for trace in trace_variants:
        for i in range(0, len(trace)-1):
            matrix[trace[i], trace[i+1]] += variants[trace]

    causal_transform_diagonal_entries(matrix, activities)

    causal_transform_nondiagonal_entries(matrix, activities)

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
    return len(log)


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
            if matrix[a, b] != 0:
                non_zero_count += 1

    return non_zero_count / (n**2)


def feature_total_no_activities(log_path):
    log = read_log(log_path)
    return len(footprints_discovery.apply(log, variant=footprints_discovery.Variants.ENTIRE_EVENT_LOG)["activities"])


def feature_percentage_concurrency(log_path):
    log = read_log(log_path)
    
    no_concurrency = len(footprints_discovery.apply(log, variant=footprints_discovery.Variants.ENTIRE_EVENT_LOG)["parallel"])
 
    return no_concurrency/(feature_total_no_activities(log_path)**2)



def feature_percentage_sequence(log_path):
    log = read_log(log_path)

    no_sequence = len(footprints_discovery.apply(log, variant=footprints_discovery.Variants.ENTIRE_EVENT_LOG)["sequence"])

    return no_sequence/(feature_total_no_activities(log_path)**2)

def feature_length_one_loops(log_path):
    activities = get_all_activities_of_log(log_path)
    n = len(activities)
    matrix = causal_matrix(log_path)

    counter = 0
    for a in activities:
        if matrix[a, a] > 0:
            counter += 1

    return counter / n


def feature_dfg_mean_variable_degree(log_path):
    G = read_networkx_graph_of_log(log_path)
    variable_degrees = list(dict(G.degree()).values())
    return np.mean(variable_degrees)

def feature_dfg_variation_coefficient_variable_degree(log_path):
    G = read_networkx_graph_of_log(log_path)
    variable_degrees = list(dict(G.degree()).values())
    return variation(variable_degrees)

def feature_dfg_min_variable_degree(log_path):
    G = read_networkx_graph_of_log(log_path)
    variable_degrees = list(dict(G.degree()).values())
    return np.min(variable_degrees)

def feature_dfg_max_variable_degree(log_path):
    G = read_networkx_graph_of_log(log_path)
    variable_degrees = list(dict(G.degree()).values())
    return np.max(variable_degrees)

def feature_dfg_entropy_variable_degree(log_path):
    G = read_networkx_graph_of_log(log_path)
    variable_degrees = list(dict(G.degree()).values())
    return entropy(variable_degrees)


def feature_dfg_wcc_variation_coefficient(log_path):
    G = read_networkx_graph_of_log(log_path)
    wcc= nx.average_clustering(G, weight='weight')
    return variation(wcc)

def feature_dfg_wcc_min(log_path):
    G = read_networkx_graph_of_log(log_path)
    wcc= nx.average_clustering(G, weight='weight')
    return np.min(wcc)

def feature_dfg_wcc_max(log_path):
    G = read_networkx_graph_of_log(log_path)
    wcc= nx.average_clustering(G, weight='weight')
    return np.max(wcc)

def feature_dfg_wcc_entropy(log_path):
    G = read_networkx_graph_of_log(log_path)
    wcc= nx.average_clustering(G, weight='weight')
    return entropy(wcc)


def compute_feature_vector(log_path):
    feature_vector = np.empty((1, len(globals.selected_features)))
    for feature_index in range(len(globals.selected_features)):
        feature_vector[0, feature_index] = compute_feature_log_path(
            log_path, feature_index)
    return feature_vector

def read_single_feature(log_path,feature_name):
    if (log_path,feature_name) in globals.features:
        return globals.features[log_path,feature_name]
    try:
        log_id = generate_log_id(log_path)
        cache_file_path = generate_cache_file(
        f"./cache/features/{feature_name}_{log_id}.pkl")
        feature = load_cache_variable(cache_file_path)
    except Exception:

        print("No cached feature vector found, now computing feature vector")
        feature = compute_feature_log_path(log_path,globals.selected_features.index(feature_name))
        store_cache_variable(feature, cache_file_path)
    return feature



def read_feature_vector(log_path):
    feature_vector = np.empty((1,len(globals.selected_features)))
    for feature_index in range(len(globals.selected_features)):
        feature_vector[0,feature_index] = read_single_feature(log_path,globals.selected_features[feature_index])
    return feature_vector


def read_feature_matrix(log_paths):
    x = np.empty((len(log_paths),
                  len(globals.selected_features)))
    for log_index in range(len(log_paths)):
        x[log_index, :] = read_feature_vector(log_paths[log_index])
    return x


def read_subset_features(log_paths):
    for log_index in range(len(log_paths)):
        globals.X[log_index, :] = read_feature_vector(log_paths[log_index])


def compute_feature_log_path(log_path, feature_index):
    feature_name = globals.selected_features[feature_index]

    # Check if the feature name is valid
    if feature_name in feature_functions:
        # Call the corresponding feature function
        ret = feature_functions[feature_name](log_path)
        return ret
    else:

        print("Invalid feature name")
        print(feature_name)
        input(feature_name)
        return None

def compute_feature(log_index, feature_index):
    log_path = globals.training_logs_paths[log_index]
    return compute_feature_log_path(log_path, feature_index)

def space_out_feature_vector_string(log_path):
    feature_vector = read_feature_vector(log_path)
    spaced_out_vector=""
    for feature_index in range(len(globals.selected_features)-1):
        spaced_out_vector = spaced_out_vector + str(feature_vector[0,feature_index]) + " "
    spaced_out_vector += str(feature_vector[0,len(globals.selected_features)-1])
    return spaced_out_vector


feature_functions = {
    "no_distinct_traces": feature_no_distinct_traces,
    "no_total_traces": feature_no_total_traces,
    "avg_trace_length": feature_avg_trace_length,
    "avg_event_repetition_intra_trace": feature_avg_event_repetition_intra_trace,
    "no_distinct_events": feature_no_distinct_events,
    "no_events_total": feature_no_events_total,
    "no_distinct_start": feature_no_distinct_start,
    "no_distinct_end": feature_no_distinct_end,
    "density": feature_density,
    "length_one_loops": feature_length_one_loops,
    "total_no_activities": feature_total_no_activities,
    "percentage_concurrency": feature_percentage_concurrency,
    "percentage_sequence": feature_percentage_sequence,
    "dfg_mean_variable_degree":feature_dfg_mean_variable_degree,
    "dfg_variation_coefficient_variable_degree":feature_dfg_variation_coefficient_variable_degree,
    "dfg_min_variable_degree":feature_dfg_min_variable_degree,
    "dfg_max_variable_degree":feature_dfg_max_variable_degree,
    "dfg_entropy_variable_degree":feature_dfg_entropy_variable_degree,
    "dfg_wcc_variation_coefficient":feature_dfg_wcc_variation_coefficient,
    "dfg_wcc_min":feature_dfg_wcc_min,
    "dfg_wcc_max":feature_dfg_wcc_max,
    "dfg_wcc_entropy":feature_dfg_wcc_entropy,
}




if __name__  == "__main__":


    log_paths = gather_all_xes("../logs/training") + gather_all_xes("../logs/testing")



    for log_path in log_paths:
        arr = read_feature_vector(log_path)
        nan_mask = np.isnan(arr)

        # Print the result
        print("Original array:")
        print(arr)

        print("\nArray with NaN check:")
        print(nan_mask)

        nan_mask = nan_mask[0]
        for i in range(len(nan_mask)):
            if nan_mask[i]:
                input(globals.selected_features[i])