###############################################################################
from utils import read_log
import pandas as pd
import pm4py
from time import time
from pm4py.objects.conversion.log import converter as log_converter
from .measures_extracted_from_literature.derived_from_linear_structures import *
from .measures_extracted_from_literature.derived_from_non_linear_structures import *
from .self_developed_measures.derived_from_linear_structures import *
from .self_developed_measures.derived_from_non_linear_structures import *
import sys
sys.path.append(
    "/rwthfs/rz/cluster/home/qc261227/Recommender/RecommenderSystem/backend/flask_app")


def feature_total_number_of_events(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return total_number_of_events(event_log)


def feature_total_number_of_event_classes(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return total_number_of_event_classes(event_log)


def feature_total_number_of_traces(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return total_number_of_traces(event_log)


def feature_total_number_of_trace_classes(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return total_number_of_trace_classes(event_log)


def feature_average_trace_length(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return average_trace_length(event_log)


def feature_minimum_trace_length(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return minimum_trace_length(event_log)


def feature_maximum_trace_length(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return maximum_trace_length(event_log)


def feature_average_trace_size(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return average_trace_size(event_log)


def feature_number_of_distinct_start_events(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return number_of_distinct_start_events(event_log)


def feature_number_of_distinct_end_events(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return number_of_distinct_end_events(event_log)


def feature_absolute_number_of_traces_with_self_loop(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return absolute_number_of_traces_with_self_loop(event_log)


def feature_absoulute_number_of_traces_with_repetition(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return absoulute_number_of_traces_with_repetition(event_log)


def feature_relative_number_of_distinct_start_events(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return relative_number_of_distinct_start_events(event_log)


def feature_relative_number_of_distinct_end_events(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return relative_number_of_distinct_end_events(event_log)


def feature_relative_number_of_traces_with_self_loop(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return relative_number_of_traces_with_self_loop(event_log)


def feature_relative_number_of_traces_with_repetition(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return relative_number_of_traces_with_repetition(event_log)


def feature_average_number_of_self_loops_per_trace(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return average_number_of_self_loops_per_trace(event_log)


def feature_maximum_number_of_self_loops_per_trace(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return maximum_number_of_self_loops_per_trace(event_log)


def feature_average_size_of_self_loops_per_trace(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return average_size_of_self_loops_per_trace(event_log)


def feature_maximum_size_of_self_loops_per_trace(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return maximum_size_of_self_loops_per_trace(event_log)


def feature_number_of_distinct_traces_per_hundred_traces(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return number_of_distinct_traces_per_hundred_traces(event_log)


def feature_absolute_trace_coverage(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return absolute_trace_coverage(event_log)


def feature_relative_trace_coverage(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return relative_trace_coverage(event_log)


def feature_event_density(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return event_density(event_log)


def feature_traces_heterogeneity_rate(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return traces_heterogeneity_rate(event_log)


def feature_trace_similarity_rate(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return trace_similarity_rate(event_log)


def feature_complexity_factor(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return complexity_factor(event_log)


def feature_simple_trace_diversity(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return simple_trace_diversity(event_log)


def feature_advanced_trace_diversity(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return advanced_trace_diversity(event_log)


def feature_trace_entropy(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return trace_entropy(event_log)


def feature_prefix_entropy(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return prefix_entropy(event_log)


def feature_all_block_entropy(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return all_block_entropy(event_log)


def feature_number_of_nodes(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return number_of_nodes(event_log)


def feature_number_of_arcs(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return number_of_arcs(event_log)


def feature_coefficient_of_network_connectivity(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return coefficient_of_network_connectivity(event_log)


def feature_average_node_degree(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return average_node_degree(event_log)


def feature_maximum_node_degree(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return maximum_node_degree(event_log)


def feature_density(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return density(event_log)


def feature_structure(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return structure(event_log)


def feature_cyclomatic_number(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return cyclomatic_number(event_log)


def feature_graph_diameter(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return graph_diameter(event_log)


def feature_number_of_cut_vertices(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return number_of_cut_vertices(event_log)


def feature_separability_ratio(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return separability_ratio(event_log)


def feature_sequentiality_ratio(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return sequentiality_ratio(event_log)


def feature_cyclicity(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return cyclicity(event_log)


def feature_affinity(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return affinity(event_log)


def feature_simple_path_complexity(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return simple_path_complexity(event_log)


def feature_start_event_frequency_evaluation(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return start_event_frequency_evaluation(event_log, 'highest_occurrence', 0.05)


def feature_end_event_frequency_evaluation(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return end_event_frequency_evaluation(event_log, 'highest_occurrence', 0.05)


def feature_event_frequency_evaluation(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return event_frequency_evaluation(event_log, 'highest_occurrence', 0.05)


def feature_trace_frequency_evaluation(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return trace_frequency_evaluation(event_log, 'highest_occurrence', 0.05)


def feature_event_dependency_evaluation(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return event_dependency_evaluation(event_log)


def feature_trace_length_evaluation(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return trace_length_evaluation(event_log)


def feature_number_of_outlying_traces(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return number_of_outlying_traces(event_log)


def feature_relative_number_of_outlying_traces(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return relative_number_of_outlying_traces(event_log)


def feature_event_profile_average_euclidean_distance(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return event_profile_average_euclidean_distance(event_log)


def feature_event_profile_average_cosine_similarity(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return event_profile_average_cosine_similarity(event_log)


def feature_transition_profile_average_euclidean_distance(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return transition_profile_average_euclidean_distance(event_log)


def feature_transition_profile_average_cosine_similarity(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return transition_profile_average_cosine_similarity(event_log)


def feature_event_profile_minimum_cosine_similarity(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return event_profile_minimum_cosine_similarity(event_log)


def feature_transition_profile_minimum_cosine_similarity(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return transition_profile_minimum_cosine_similarity(log_path)


def feature_average_spatial_proximity(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return average_spatial_proximity(event_log)


def feature_spatial_proximity_connectedness(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return spatial_proximity_connectedness(event_log)


def feature_spatial_proximity_abstraction_evaluation(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return spatial_proximity_abstraction_evaluation(event_log)


def feature_event_dependency_abstraction_evaluation(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return event_dependency_abstraction_evaluation(event_log)


def feature_triple_abstraction_evaluation(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return triple_abstraction_evaluation(event_log)


def feature_event_class_triple_abstraction_evaluation(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return event_class_triple_abstraction_evaluation(event_log)


def feature_number_of_graph_communities(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return number_of_graph_communities(event_log)


def feature_maximum_cut_vertex_outgoing_degree(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return maximum_cut_vertex_outgoing_degree(event_log)


def feature_cut_vertex_independent_path(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return cut_vertex_independent_path(event_log)


def feature_simple_path_minimum_jaccard_similarity(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return simple_path_minimum_jaccard_similarity(event_log)


def feature_syntactic_node_similarity(log_path):
    event_log = pm4py.format_dataframe(read_log(log_path))
    event_log = log_converter.apply(event_log)
    return syntactic_node_similarity(event_log)


# print(feature_total_number_of_traces("../../logs/training/989649610.xes"))
