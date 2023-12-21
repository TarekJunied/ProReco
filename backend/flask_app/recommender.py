import globals
# from feature_controller import read_optimal_features
from measures import read_measure_entry
from multiobjective import predicted_classification_based_scalarization, predicted_regression_based_scalarization
from feature_controller import get_total_feature_functions_dict
from classifiers import read_fitted_classifier, compute_fitted_classifier
from regressors import read_fitted_regressor, compute_fitted_regressor
from binary_classifiers import read_fitted_binary_classifier, get_all_pairs_of_algorithms, compute_fitted_binary_classifier
from filehelper import gather_all_xes, get_all_ready_logs, clear_cached_regressors, clear_cached_binary_classifiers, clear_cached_classifiers
from init import init_given_parameters

current_mode = "predicted_regression_based_scalarization"


def final_prediction(log_path_to_predict, measure_weight):
    if current_mode == "predicted_regression_based_scalarization":
        dict = predicted_regression_based_scalarization(log_path_to_predict, "random_forest", measure_weight, [
        ], globals.selected_features, globals.algorithm_portfolio)

    elif current_mode == "predicted_classification_based_scalarization":
        dict = predicted_classification_based_scalarization(log_path_to_predict, "random_forest", measure_weight, [
        ], globals.selected_features, globals.algorithm_portfolio)

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


if __name__ == "__main__":

    # clear_cached_classifiers()
    # clear_cached_binary_classifiers()
    # clear_cached_regressors()
    globals.measures_list = [
        "token_fitness", "token_precision", "generalization", "pm4py_simplicity"]
    globals.algorithm_portfolio = [
        "alpha", "inductive", "heuristic", "split", "ILP"]

    feature_dict = get_total_feature_functions_dict()

    feature_list = list(feature_dict.keys())

    globals.selected_features = feature_list

    algorithm_portfolio = globals.algorithm_portfolio

    load_all_needed_classifiers_and_regressors()
