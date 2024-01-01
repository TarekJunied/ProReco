def get_removed_features_list():
    # these features appear in the exact same format under another name
    redundant_features = [
        "no_events_total",
        "total_number_of_trace_classes",
        "no_distinct_traces",
        "total_number_of_event_classes",
        "no_distinct_events",
        "total_no_activities",
        "number_of_distinct_start_events",
        "no_distinct_start",
        "number_of_distinct_end_events",
        "no_distinct_end",
        "average_trace_length",
        "coefficient_of_network_connectivity",
        "event_profile_minimum_cosine_similarity",
        "event_profile_average_cosine_similarity",
        "event_profile_average_euclidean_distance",
        "transition_profile_average_euclidean_distance",
    ]
    removed_features = redundant_features + []
    return removed_features

# "total_number_of_trace_classes" => ""
