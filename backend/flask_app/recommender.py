import globals
# from feature_controller import read_optimal_features


import pm4py
import threading
from measures import read_measure_entry
from utils import read_log
from multiobjective import predicted_classification_based_scalarization, predicted_regression_based_scalarization
from feature_controller import get_total_feature_functions_dict, read_feature_vector
from classifiers import read_fitted_classifier, compute_fitted_classifier
from regressors import read_fitted_regressor, compute_fitted_regressor, regression
from binary_classifiers import read_fitted_binary_classifier, get_all_pairs_of_algorithms, compute_fitted_binary_classifier
from filehelper import gather_all_xes, get_all_ready_logs, clear_cached_regressors, clear_cached_binary_classifiers, clear_cached_classifiers
from utils import read_model
from explainer import get_decision_plot_dict_
from init import init_given_parameters
from petri_net import create_json_petri_net
from output_manager import progressed_read_log
from LogGenerator.log_generator import create_random_log, create_random_process, create_log_from_model
current_mode = "predicted_regression_based_scalarization"


def final_prediction(log_path_to_predict, measure_weight):

    globals.set_progress_state(log_path_to_predict, "parsing")
    print("now starting parsing")
    globals.set_parse_percentage(log_path_to_predict, 0)
    progressed_read_log(log_path_to_predict)
    globals.set_progress_state(log_path_to_predict, "featuring")
    read_feature_vector(log_path_to_predict, globals.selected_features)
    globals.set_progress_state(log_path_to_predict, "predicting")

    if current_mode == "predicted_regression_based_scalarization":
        dict = predicted_regression_based_scalarization(log_path_to_predict, globals.regression_method, measure_weight, [
        ], globals.selected_features, globals.algorithm_portfolio)

    elif current_mode == "predicted_classification_based_scalarization":
        dict = predicted_classification_based_scalarization(log_path_to_predict, globals.classification_method, measure_weight, [
        ], globals.selected_features, globals.algorithm_portfolio)

    else:
        print("invalid prediction mode")

    globals.set_progress_state(log_path_to_predict, "done")

    return dict


def finale_schnitstelle_hier():
    return 0


def load_all_needed_classifiers_and_regressors():

    all_logs = gather_all_xes("../logs/training") + gather_all_xes(
        "../logs/testing") + gather_all_xes("../logs/modified_eventlogs")
    ready_training = get_all_ready_logs(
        all_logs, globals.selected_features, globals.algorithm_portfolio, globals.measures_list)

    input(len(ready_training))

    init_given_parameters(
        ready_training, globals.algorithm_portfolio, feature_list, globals.measures_list)

    algorithm_pairs = get_all_pairs_of_algorithms(globals.algorithm_portfolio)

    for classification_method in globals.classification_methods:
        for measure_name in globals.measures_list:
            read_fitted_classifier(classification_method,
                                   measure_name, ready_training, globals.selected_features)

    for regression_method in globals.regression_methods:
        for measure_name in globals.measures_list:
            for discovery_algorithm in globals.algorithm_portfolio:
                read_fitted_regressor(
                    regression_method, discovery_algorithm, measure_name, ready_training, globals.selected_features)

    for binary_classification_method in globals.binary_classification_methods:
        for measure_name in globals.measures_list:
            for (algorithm_a, algorithm_b) in algorithm_pairs:
                read_fitted_binary_classifier(
                    binary_classification_method,   algorithm_a, algorithm_b, measure_name, ready_training, globals.selected_features)


def get_final_petri_net_dict(log_path, discovery_algorithm):
    print(
        f"now starting to compute model for {log_path} using {discovery_algorithm}")
    petri_net = read_model(log_path, discovery_algorithm)
    print("now starting to create_json_petri_net")
    petri_net_dict = create_json_petri_net(petri_net)
    print("returning: ")
    print(petri_net_dict)
    return petri_net_dict


def create_random_processs_dict(slider_values):
    process = create_random_process(slider_values["andBranches"], slider_values["xorBranches"], slider_values["loopWeight"], slider_values["singleActivityWeight"], slider_values["skipWeight"], slider_values["sequenceWeight"], slider_values["andWeight"],
                                    slider_values["xorWeight"], slider_values["maxDepth"], slider_values["dataObjectProbability"])
    return process


def create_random_log_dict(slider_values, session_token):
    log_path = f"../logs/frontend/{session_token}.xes"
    globals.set_progress_state(log_path, "creatingProcess")
    print("now creating Process state")
    model_path = create_random_processs_dict(slider_values)
    globals.set_progress_state(log_path, "creatingLog")
    print("now creating log state")

    create_log_from_model(model_path, log_path,
                          slider_values["numberOfTraces"])
    globals.set_progress_state(log_path, "done")
    print("now done state")


def get_regressed_algo_measure_dict(log_path):
    dict = {}
    for measure in globals.measures_list:
        for discovery_algorithm in globals.algorithm_portfolio:
            dict[f"{discovery_algorithm}-{measure}"] = round(regression(
                log_path, globals.regression_method, discovery_algorithm, measure, [], globals.selected_features), 2)

    return dict


def get_decision_plot_dict(log_path_to_explain):
    ret_dict = {}
    regression_method = globals.regression_method
    for discovery_algorithm in globals.algorithm_portfolio:
        for measure in globals.measures_list:
            ret_dict[f"{discovery_algorithm}-{measure}"] = get_decision_plot_dict_(
                log_path_to_explain, regression_method, discovery_algorithm, [], measure, globals.selected_features)
    return ret_dict


if __name__ == "__main__":

    clear_cached_regressors()
    input("done")

    hi = {'andBranches': 4, 'xorBranches': 2, 'loopWeight': 0.42, 'singleActivityWeight': 0.64, 'skipWeight': 0.5,
          'sequenceWeight': 0.41, 'andWeight': 0.37, 'xorWeight': 0.39, 'maxDepth': 2, 'dataObjectProbability': 0.55, 'numberOfTraces': 1868}

    globals.measures_list = [
        "token_fitness", "token_precision", "generalization", "pm4py_simplicity"]
    globals.algorithm_portfolio = [
        "alpha", "inductive", "heuristic", "split", "ILP"]

    feature_dict = get_total_feature_functions_dict()

    feature_list = list(feature_dict.keys())

    globals.selected_features = feature_list

    algorithm_portfolio = globals.algorithm_portfolio

    log_paths = gather_all_xes("../logs/real_life_logs")

    log_path = log_paths[1]

    progressed_read_log(log_path)

    # After the thread finishes, you can access the captured_stderr_output
