import shap
import os
import sys
import globals
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import load_cache_variable, store_cache_variable
from regressors import read_fitted_regressor, regression, compute_fitted_regressor
from classifiers import read_fitted_classifier
from feature_controller import read_feature_matrix, get_total_feature_functions_dict, read_feature_vector
from feature_selection import regression_read_optimal_features
from filehelper import gather_all_xes, get_all_ready_logs
from init import init_given_parameters


def compute_fitted_explainer(regression_method, discovery_algorithm, measure_name):
    model = read_fitted_regressor(
        regression_method, discovery_algorithm, measure_name, [])

    explainer = shap.TreeExplainer(model)

    return explainer


def read_regression_shap_explainer(regression_method, discovery_algorithm, measure_name):

    cache_file_path = f"./cache/explainers/{regression_method}_{discovery_algorithm}_{measure_name}.pkl"
    try:
        explainer = load_cache_variable(cache_file_path)
    except Exception as e:
        store_dir = "./cache/explainers/"
        os.makedirs(store_dir, exist_ok=True)
        explainer = compute_fitted_explainer(
            regression_method, discovery_algorithm, measure_name)
        store_cache_variable(explainer, cache_file_path)

    return explainer


def get_decision_plot_dict_(log_path_to_explain, regression_method, discovery_algorithm,  measure_name):

    feature_portfolio = regression_read_optimal_features(
        [], regression_method, discovery_algorithm, measure_name, [])

    explainer = read_regression_shap_explainer(
        regression_method, discovery_algorithm, measure_name)

    x_test = pd.DataFrame(read_feature_vector(
        log_path_to_explain, feature_portfolio).reshape(1, -1), columns=feature_portfolio)

    shap_values_instance = explainer.shap_values(x_test)

    # Find the indices of the top 10 absolute SHAP values
    top_indices = np.argsort(-np.abs(shap_values_instance[0]))[:10]

    # Get the names of the top 10 features
    top_features = list(x_test.columns[top_indices])

    top_feature_values = list(x_test.iloc[0, top_indices].values)

    # Get the corresponding SHAP values for the top 10 features
    top_shap_values = shap_values_instance[0][top_indices]

    # Subset the x_test to only include the top 10 features
    x_test_top_features = x_test.iloc[0, top_indices].values.reshape(1, -1)
    """"
    plt.clf()

    expected_value = explainer.expected_value


    # Create a SHAP decision plot for the top 10 features
    shap.decision_plot(explainer.expected_value, top_shap_values, x_test_top_features,
                       feature_names=top_features, highlight=0)

    # Save the figure as a .png file
    plt.tight_layout(pad=3.0)

    plt.axvline(x=expected_value, linestyle="--",
                color="red")  # Base value line
    plt.axvline(x=expected_value + shap_values_instance.sum(),
                linestyle="--", color="green")  # Final prediction line

    plt.savefig(
        f"shap_decision_plot_top10_{regression_method}.png", format='png', dpi=300)
    """
    plot_values = [float(explainer.expected_value)]
    i = 0

    top_shap_values_descendigly = list(top_shap_values)
    top_shap_values_descendigly.reverse()

    for shap_value in top_shap_values_descendigly:
        plot_values += [float(plot_values[i] + shap_value)]
        i += 1

    ret_dict = {"plot_values": plot_values,
                "predicted_value": explainer.model.predict(x_test)[0],
                "top_features": top_features+["expected value"],
                "feature_values": top_feature_values,
                "labels": top_features+["expected value"]}

    # Optionally, you might want to save or return this information
    return ret_dict


if __name__ == "__main__":

    log_paths = gather_all_xes("../logs/modified_eventlogs")

    for discovery_algorithm in globals.algorithm_portfolio:
        for measure in globals.measure_portfolio:
            x = get_decision_plot_dict_(
                log_paths[0], "xgboost", discovery_algorithm, measure)
            input(x)
