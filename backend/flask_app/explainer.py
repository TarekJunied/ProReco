import shap
import sys
import globals
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_cache_variable, store_cache_variable
from recommender import read_fitted_classifier
from feature_controller import read_feature_matrix, get_total_feature_functions_dict, read_feature_vector
from filehelper import gather_all_xes, get_all_ready_logs_multiple
from init import init_given_parameters
from feature_selection import read_optimal_features


def read_shap_explainer(classification_method, ready_training, measure_name, feature_portfolio):
    cache_file_path = f"./cache/explainers/{classification_method}_{measure_name}.pkl"
    x_train = read_feature_matrix(ready_logs, feature_portfolio)
    try:
        explainer = load_cache_variable(cache_file_path)
    except Exception as e:
        clf = read_fitted_classifier(
            classification_method, measure_name, ready_training, feature_portfolio)

        if classification_method in ["decision_tree", "random_forest", "xgboost"]:
            explainer = shap.TreeExplainer(clf)
        elif classification_method == "knn" or classification_method == "svm" or classification_method == "logistic_regression":
            explainer = shap.KernelExplainer(clf.predict_proba, x_train)
        elif classification_method == "svm":
            explainer = shap.KernelExplainer(clf.predict_proba, x_train)
        else:
            print("no shap values possible for this classification method")
            sys.exit(-1)

        store_cache_variable(explainer, cache_file_path)

    return explainer


def create_shap_graph(ready_training, testing_instance_log_path, classification_method, measure_name, feature_portfolio):
    # Assuming read_feature_vector and read_shap_explainer are defined elsewhere
    x_test = read_feature_vector(testing_instance_log_path, feature_portfolio)
    x_test = pd.DataFrame(x_test, columns=feature_portfolio)

    explainer = read_shap_explainer(
        classification_method, ready_training, measure_name, feature_portfolio)
    shap_values = explainer.shap_values(x_test)

    # Plot the SHAP summary bar plot
    shap.summary_plot(shap_values, x_test,
                      feature_names=feature_portfolio, plot_type="bar", show=False)

    # Save the plot
    storage_dir = "../evaluation/shap"
    plt.savefig(
        f'{storage_dir}/{classification_method}_{measure_name}_shap_summary_plot.png', bbox_inches='tight')

    # Optionally, clear the current plot to free memory
    plt.clf()


if __name__ == "__main__":
    shap.initjs()
    globals.algorithm_portfolio = [
        "alpha", "inductive", "heuristic", "split", "ILP"]
    feature_dict = get_total_feature_functions_dict()

    feature_list = list(feature_dict.keys())

    globals.selected_features = feature_list
    globals.measures_list = ["token_fitness", "token_precision",
                             "no_total_elements", "generalization", "pm4py_simplicity"]

    globals.classification_methods = [
        x for x in globals.classification_methods if x not in ["knn", "svm"]]

    all_logs = gather_all_xes("../logs/training") + gather_all_xes(
        "../logs/testing") + gather_all_xes("../logs/modified_eventlogs")
    ready_logs = get_all_ready_logs_multiple(all_logs[:100])

    token_precision_optimal_features = read_optimal_features(
        [], "xgboost", "token_precision", feature_list, globals.algorithm_portfolio)
    create_shap_graph(ready_logs, ready_logs[0], "random_forest",
                      "token_precision", token_precision_optimal_features)

    # init_given_parameters(ready_logs, globals.algorithm_portfolio, feature_list, globals.measures_list)
