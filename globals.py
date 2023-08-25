algorithm_portfolio = ["alpha","heuristic","inductive"]
features_list = ["no_distinct_traces","no_total_traces","avg_trace_length","avg_event_repetition_intra_trace","no_distinct_events"
                 ,"no_events_total","no_distinct_start","no_distinct_end","causality_strength","density","length_one_loops"]

selected_features = ["no_distinct_traces","no_total_traces","avg_trace_length","avg_event_repetition_intra_trace","no_distinct_events"
                 ,"no_events_total","no_distinct_start","no_distinct_end","causality_strength","density","length_one_loops"]

models = {}
log_paths = []
logs = {}
cached_variables = {}
y = None

X = None

no_logs = 4