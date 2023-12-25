
import os


flask_app_path = "/Users/tarekjunied/Documents/Universität/BachelorThesis/backend/flask_app"
flask_app_path = "/home/qc261227/Recommender/RecommenderSystem/backend/flask_app"
flask_app_path = os.environ.get("PRORECO_FLASK")
new_algos = ["alpha_plus", "inductive_infrequent", "inductive_direct"]
algorithm_portfolio = ["alpha", "heuristic",
                       "inductive", "ILP", "split"] + new_algos
classification_method = "xgboost"

regression_method = "random_forest"


selected_features = ["no_distinct_traces", "no_total_traces", "avg_trace_length", "avg_event_repetition_intra_trace",
                     "no_distinct_events", "no_events_total", "no_distinct_start", "no_distinct_end", "density", "length_one_loops", "total_no_activities", "percentage_concurrency", "percentage_sequence",
                     "dfg_mean_variable_degree",
                     "dfg_variation_coefficient_variable_degree",
                     "dfg_min_variable_degree",
                     "dfg_max_variable_degree",
                     "dfg_entropy_variable_degree",
                     "dfg_wcc_min",
                     "dfg_wcc_max",
                     "dfg_wcc_entropy",
                     "dfg_wcc_variation_coefficient"
                     ]
# selected_features = fig4pm_features

# "alignment_precision": "max" "alignment_fitness": "max", used_memory": "min",
measures_kind = {"token_fitness": "max", "token_precision": "max",
                 "no_total_elements": "min", "node_arc_degree": "min", "runtime": "min",  "generalization": "max", "pm4py_simplicity": "max", "log_runtime": "min"}
# ,"log_runtime"
measures_list = ["token_fitness",  "token_precision",
                 "no_total_elements", "node_arc_degree", "runtime", "generalization", "pm4py_simplicity", "log_runtime"]

normalisierbare_measures = {"token_fitness": "max",  "token_precision": "max",
                            "generalization": "max", "pm4py_simplicity": "max"}

binary_classification_methods = [
    "decision_tree",
    "knn",
    "svm",
    "random_forest",
    "logistic_regression",
    "gradient_boosting",
    "xgboost",
    "mlp",
    "adaboost",
    "extra_trees",
    "gaussian_nb",
    "ridge",
    "sgd",
    "passive_aggressive"
]
# logistic regression removed, "autofolio"
# "knn", "svm",
classification_methods = ["decision_tree",
                          "random_forest", "logistic_regression", "gradient_boosting",  "xgboost"]

regression_methods = [
    "linear_regression",
    "ridge_regression",
    "lasso_regression",
    "decision_tree",
    "random_forest",
    "gradient_boosting",
    "svm",
    "knn",
    "mlp",
    "xgboost"
]

features = {}
training_log_paths = {}
testing_log_paths = {}
log_paths = {}
measures = {}
models = {}


progress_dict = {}


def get_log_name(log_path):
    return split_file_path(log_path)["filename"]


def split_file_path(file_path):
    # Split the file path into directory, filename, and extension
    directory, file_name_with_extension = os.path.split(file_path)
    file_name, file_extension = os.path.splitext(file_name_with_extension)

    return {
        'directory': directory,
        'filename': file_name,
        'extension': file_extension
    }


def translate_feature_name(feature_name):

    # Replace underscores with spaces
    spaced_string = feature_name.replace("_", " ")

    # Split the string into words
    words = spaced_string.split()

    # Capitalize the first letter of each word
    capitalized_words = [word.capitalize() for word in words]

    # Join the words back into a single string
    formatted_string = " ".join(capitalized_words)

    return formatted_string


def init_progress_dict(log_path):
    log_name = get_log_name(log_path)
    if log_name not in progress_dict:
        progress_dict[log_name] = {}


def set_progress_state(log_path, state):
    log_name = get_log_name(log_path)
    init_progress_dict(log_path)
    progress_dict[log_name]["state"] = state


def set_progress_current_feature_name_and_percentage(log_path, feature_name):
    log_name = get_log_name(log_path)
    init_progress_dict(log_path)
    progress_dict[log_name]["current_feature_name"] = translate_feature_name(
        feature_name)
    index_of_feature = selected_features.index(feature_name)
    progress_dict[log_name]["feature_progress"] = round((
        index_of_feature + 1) / len(selected_features), 2)*100


def set_parse_percentage(log_path, progress_percentage):
    log_name = get_log_name(log_path)
    init_progress_dict(log_path)
    progress_dict[log_name]["parse_progress"] = progress_percentage
    print("now got new percentage: ", progress_percentage)


def get_progress_dict_of_session_token(session_token):
    if session_token not in progress_dict:
        return "no progress yet"
    return progress_dict[session_token]
