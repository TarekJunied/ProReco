home_dir = "/Users/tarekjunied/Documents/Universität/BachelorThesis"
algorithm_portfolio = ["alpha", "heuristic",
                       "inductive", "ILP", "split"]

#    "dfg_wcc_variation_coefficient",
#   "dfg_wcc_entropy"
selected_features = ["no_distinct_traces", "no_total_traces", "avg_trace_length", "avg_event_repetition_intra_trace",
                     "no_distinct_events", "no_events_total", "no_distinct_start", "no_distinct_end", "density", "length_one_loops","total_no_activities","percentage_concurrency","percentage_sequence",
    "dfg_mean_variable_degree",
    "dfg_variation_coefficient_variable_degree",
    "dfg_min_variable_degree",
    "dfg_max_variable_degree",
    "dfg_entropy_variable_degree",

    "dfg_wcc_min",
    "dfg_wcc_max",
 ]

## "alignment_precision": "max" "alignment_fitness": "max", used_memory": "min",
measures_kind = {"token_fitness": "max", "token_precision": "max",
            "no_total_elements": "min", "node_arc_degree": "min", "runtime": "min",  "generalization": "max", "pm4py_simplicity": "max","log_runtime":"min"}
# ,"log_runtime"
measures_list = ["token_fitness",  "token_precision", 
                 "no_total_elements", "node_arc_degree", "runtime", "generalization", "pm4py_simplicity","log_runtime"]

normalisierbare_measures = {"token_fitness": "max", "alignment_fitness": "max", "token_precision": "max",
                            "alignment_precision": "max",  "generalization": "max", "pm4py_simplicity": "max"}


#logistic regression removed
classification_methods = ["decision_tree", "knn", "svm",
                          "random_forest", "gradient_boosting","autofolio"]

selected_measure = "token_precision"
working_dir = "/Users/tarekjunied/Documents/Universität/BachelorThesis"
features = {}
training_log_paths = {}
testing_log_paths = {}
measures = {}
models = {}

