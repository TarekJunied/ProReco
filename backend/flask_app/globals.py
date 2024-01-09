
import os
import pickle

flask_app_path = "/Users/tarekjunied/Documents/Universität/BachelorThesis/backend/flask_app"
flask_app_path = "/home/qc261227/Recommender/RecommenderSystem/backend/flask_app"
flask_app_path = os.environ.get("PRORECO_FLASK")
algorithm_portfolio = ["alpha", "heuristic",
                       "inductive", "ILP", "split", "alpha_plus", "inductive_infrequent", "inductive_direct"]
classification_method = "xgboost"

regression_method = "xgboost"

feature_portfolio_file_path = "./constants/feature_portfolio.pk"
with open(feature_portfolio_file_path, 'rb') as file:
    feature_portfolio = pickle.load(file)

used_feature_portfolio_file_path = "./constants/used_feature_portfolio.pk"
with open(feature_portfolio_file_path, 'rb') as file:
    used_feature_portfolio = pickle.load(file)


# "alignment_precision": "max" "alignment_fitness": "max", used_memory": "min",
measures_kind = {"token_fitness": "max", "token_precision": "max",
                 "no_total_elements": "min", "node_arc_degree": "min", "runtime": "min",  "generalization": "max", "pm4py_simplicity": "max", "log_runtime": "min"}
# ,"log_runtime"
measure_portfolio = ["token_fitness",  "token_precision",
                     "generalization", "pm4py_simplicity"]

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
#    "ridge_regression",    "lasso_regression",
regression_methods = [
    "random_forest",
    "svm",
    "xgboost"
]

features = {}
training_log_paths = {}
testing_log_paths = {}
log_paths = {}
measures = {}
models = {}
regressors = {}

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
    index_of_feature = used_feature_portfolio.index(feature_name)
    new_val = round((
        index_of_feature + 1) / len(used_feature_portfolio), 2)*100
    if new_val >= 0 and new_val <= 100:
        progress_dict[log_name]["feature_progress"] = new_val


def set_parse_percentage(log_path, progress_percentage):
    log_name = get_log_name(log_path)
    init_progress_dict(log_path)
    progress_dict[log_name]["parse_progress"] = progress_percentage
    print("now got new percentage: ", progress_percentage)


def get_progress_dict_of_session_token(session_token):
    if session_token not in progress_dict:
        return "no progress yet"
    return progress_dict[session_token]
