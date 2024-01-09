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
from feature_evaluation import read_single_feature_information_dict
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
    read_feature_vector(log_path_to_predict, globals.used_feature_portfolio)
    globals.set_progress_state(log_path_to_predict, "predicting")

    dict = predicted_regression_based_scalarization(log_path_to_predict, globals.regression_method, measure_weight, [
    ], globals.feature_portfolio, globals.algorithm_portfolio)

    globals.set_progress_state(log_path_to_predict, "done")

    return dict


def finale_schnitstelle_hier():
    return 0


def load_all_needed_classifiers_and_regressors():

    all_logs = gather_all_xes("../logs/training") + gather_all_xes(
        "../logs/testing") + gather_all_xes("../logs/modified_eventlogs")
    ready_training = get_all_ready_logs(
        all_logs, globals.feature_portfolio, globals.algorithm_portfolio, globals.measure_portfolio)

    input(len(ready_training))

    init_given_parameters(
        ready_training, globals.algorithm_portfolio, feature_list, globals.measure_portfolio)

    algorithm_pairs = get_all_pairs_of_algorithms(globals.algorithm_portfolio)

    for classification_method in globals.classification_methods:
        for measure_name in globals.measure_portfolio:
            read_fitted_classifier(classification_method,
                                   measure_name, ready_training, globals.feature_portfolio)

    for regression_method in globals.regression_methods:
        for measure_name in globals.measure_portfolio:
            for discovery_algorithm in globals.algorithm_portfolio:
                read_fitted_regressor(
                    regression_method, discovery_algorithm, measure_name, ready_training, globals.feature_portfolio)

    for binary_classification_method in globals.binary_classification_methods:
        for measure_name in globals.measure_portfolio:
            for (algorithm_a, algorithm_b) in algorithm_pairs:
                read_fitted_binary_classifier(
                    binary_classification_method,   algorithm_a, algorithm_b, measure_name, ready_training, globals.feature_portfolio)


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
    for measure in globals.measure_portfolio:
        for discovery_algorithm in globals.algorithm_portfolio:
            dict[f"{discovery_algorithm}-{measure}"] = round(regression(
                log_path, globals.regression_method, discovery_algorithm, measure, []), 2)

    return dict
# Function to get the sorted list


def sort_features_by_no_regressors(feature_list):
    sorted_list = sorted(
        feature_list, key=lambda x: x['no_regressors'], reverse=True)
    return sorted_list


def get_decision_plot_dict(log_path_to_explain):
    ret_dict = {}
    regression_method = globals.regression_method
    for discovery_algorithm in globals.algorithm_portfolio:
        for measure in globals.measure_portfolio:
            ret_dict[f"{discovery_algorithm}-{measure}"] = get_decision_plot_dict_(
                log_path_to_explain, regression_method, discovery_algorithm, measure)
    return ret_dict


def get_feature_information_dict():
    ret_list = []
    for feature in globals.feature_portfolio:
        ret_list += [read_single_feature_information_dict(feature)]

    return sort_features_by_no_regressors(ret_list)


if __name__ == "__main__":

    log_paths = gather_all_xes("../logs/frontend")
    log_path = log_paths[0]
    input(get_feature_information_dict())
