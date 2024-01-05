import shap
import sys
import globals
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import load_cache_variable, store_cache_variable
from regressors import read_fitted_regressor, regression, compute_fitted_regressor
from classifiers import read_fitted_classifier
from feature_controller import read_feature_matrix, get_total_feature_functions_dict, read_feature_vector
from filehelper import gather_all_xes, get_all_ready_logs
from init import init_given_parameters
from feature_controller import read_single_feature


def read_classification_shap_explainer(classification_method, ready_training, measure_name, feature_portfolio):
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


def select_shap_explainer(regression_method, model, X_train):
    """
    Selects and returns the appropriate SHAP explainer based on the model type.
    """

    if regression_method in ["decision_tree", "random_forest", "gradient_boosting", "xgboost"]:
        return shap.TreeExplainer(model)
    elif regression_method in ["linear_regression", "ridge_regression", "lasso_regression"]:
        return shap.LinearExplainer(model, X_train)
    # KernelExplainer can be slow and should be used if no better alternative
    elif regression_method in ["svm", "knn", "mlp"]:
        return shap.KernelExplainer(model.predict, X_train)
    else:
        raise ValueError(
            f"No appropriate SHAP explainer for the specified model: {model}")


def compute_fitted_explainer(regression_method, discovery_algorithm, measure_name, ready_training, feature_portfolio):
    x_train = pd.DataFrame(read_feature_matrix(
        ready_training, feature_portfolio), columns=feature_portfolio)

    model = compute_fitted_regressor(
        regression_method, discovery_algorithm, measure_name, ready_training)

    explainer = select_shap_explainer(regression_method, model, x_train)

    return explainer


def read_regression_shap_explainer(regression_method, discovery_algorithm, ready_training, measure_name, feature_portfolio):
    cache_file_path = f"./cache/explainers/{regression_method}_{measure_name}.pkl"
    try:
        explainer = load_cache_variable(cache_file_path)
    except Exception as e:

        explainer = compute_fitted_explainer(
            regression_method, discovery_algorithm, measure_name, ready_training, feature_portfolio)
        store_cache_variable(explainer, cache_file_path)

    return explainer


def get_decision_plot_dict_(log_path_to_explain, regression_method, discovery_algorithm, ready_training, measure_name, feature_portfolio):

    explainer = read_regression_shap_explainer(
        regression_method, discovery_algorithm, ready_training, measure_name, feature_portfolio)

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
    plot_values = [explainer.expected_value[0]]
    i = 0

    top_shap_values_descendigly = list(top_shap_values)
    top_shap_values_descendigly.reverse()

    for shap_value in top_shap_values_descendigly:
        plot_values += [plot_values[i] + shap_value]
        i += 1

    ret_dict = {"plot_values": plot_values,
                "predicted_value": explainer.model.predict(x_test)[0],
                "top_features": top_features+["expected value"],
                "feature_values": top_feature_values,
                "labels": top_features+["expected value"]}

    # Optionally, you might want to save or return this information
    return ret_dict


if __name__ == "__main__":
    all_logs = gather_all_xes("../logs/training") + gather_all_xes(
        "../logs/testing") + gather_all_xes("../logs/modified_eventlogs")
    all_logs = all_logs[:20]
    ready_logs = get_all_ready_logs(
        all_logs, globals.feature_portfolio, globals.algorithm_portfolio, globals.measure_portfolio)

    init_given_parameters(ready_logs, globals.algorithm_portfolio,
                          globals.feature_portfolio, globals.measure_portfolio)

    for discovery_algorithm in globals.algorithm_portfolio:
        for measure in globals.measure_portfolio:
            read_regression_shap_explainer(
                globals.regression_method, discovery_algorithm, ready_logs, measure, globals.feature_portfolio)
