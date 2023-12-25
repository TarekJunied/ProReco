import pandas as pd
import math
import os
import seaborn as sns
import matplotlib.pyplot as plt
import globals
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import SelectKBest, chi2
from filehelper import gather_all_xes, get_all_logs_with_ready_features, get_all_ready_logs
from flask_app.feature_controller import read_feature_matrix
from feature_controller import get_total_feature_functions_dict, read_single_feature
from classifiers import compute_fitted_classifier, read_fitted_classifier
from measures import read_classification_target_vector
from init import load_logs_into_main_memory, load_features_into_main_memory, load_measures_into_main_main_memory, fix_corrupt_cache, init_given_parameters
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.feature_selection import RFE
from sklearn.feature_selection import RFECV
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score
from utils import generate_log_id, generate_cache_file, store_cache_variable, load_cache_variable


# Assuming X and y are your features and target variable


def list_feature_correlations(ready_logpaths):

    X = read_feature_matrix(ready_logpaths)

    # Convert the numpy array 'X' to a DataFrame for easier manipulation
    # Assuming 'feature_names' contains the names of the features
    feature_matrix = pd.DataFrame(X, columns=globals.selected_features)
    # Calculate the correlation matrix
    corr_matrix = feature_matrix.corr()
    correlations = []

    # Iterate over the matrix to extract the correlations
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):  # Avoid double-counting pairs
            if not math.isnan(corr_matrix.iloc[i, j]):
                correlations.append(
                    (corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j]))

    # Sort the list by absolute correlation value, in descending order
    correlations.sort(key=lambda x: abs(x[2]), reverse=True)

    file_path = "./correlations.txt"
    # Open a file to save the sorted results
    with open(file_path, 'w') as file:
        for corr in correlations:
            file.write(f"{corr[0]}, {corr[1]}, {corr[2]:.4f}\n")


def plot_feature_correlation(ready_logpaths):
    X = read_feature_matrix(ready_logpaths)

    # Convert the numpy array 'X' to a DataFrame for easier manipulation
    # Assuming 'feature_names' contains the names of the features
    feature_matrix = pd.DataFrame(X, columns=globals.selected_features)

    # Calculate the correlation matrix
    corr = feature_matrix.corr()

    # Set up the matplotlib figure with a suitable size for 200 features
    plt.figure(figsize=(90, 600))

    # Draw the heatmap
    sns.heatmap(corr,
                xticklabels=corr.columns,
                yticklabels=corr.columns,
                cmap='coolwarm',    # You can choose a different colormap
                annot=False,        # Set to True if you want to see the correlation values
                linewidths=.5)

    # Adding labels and title for clarity
    plt.title('Feature Correlations', fontsize=30)
    plt.xlabel('Features', fontsize=30)
    plt.ylabel('Features', fontsize=30)

    # Adjusting tick labels for readability
    plt.xticks(rotation=90, fontsize=8)
    plt.yticks(rotation=0, fontsize=8)

    # Save the plot
    plt.savefig(
        f"../evaluation/feature_correlation/{len(globals.selected_features)}_correlation.png")


def plot_feature_importance_on_measure(ready_logpaths, feature_names, measure_name):
    X = read_feature_matrix(ready_logpaths)

    y = read_classification_target_vector(
        ready_logpaths, measure_name, globals.algorithm_portfolio)

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # Converting the numpy array 'X' to a DataFrame for easier manipulation
    # Generating feature names
    feature_matrix = pd.DataFrame(X, columns=feature_names)

    # Calculating feature importance using a basic method like Mean Absolute Correlation
    feature_importance = feature_matrix.apply(
        lambda col: col.corr(pd.Series(y_encoded))).abs()
    feature_importance_sorted = feature_importance.sort_values(ascending=False)

  # Create a bar plot
    plt.figure(figsize=(20, 12))
    sns.barplot(x=feature_importance_sorted.values,
                y=feature_importance_sorted.index, orient='h')

    # Adding labels and title for clarity
    plt.xlabel('Importance')
    plt.ylabel('Features')
    plt.title('Feature Importance')
    plt.savefig(
        f"../evaluation/feature_importance/{measure_name}_{len(feature_names)}.png")


def classification_select_k_best_features(log_paths, algorithm_portfolio, feature_portfolio, measure_name, k=100):
    X_train = read_feature_matrix(log_paths, feature_portfolio)
    y_train = read_classification_target_vector(
        log_paths, measure_name, algorithm_portfolio)
    selector_anova = SelectKBest(f_classif, k=k)

    # Fit the selector to the data
    X_anova_selected = selector_anova.fit_transform(X_train, y_train)

    # Now you can use get_support() as the selector is fitted
    selected_features_mask = selector_anova.get_support()

    feature_names = globals.selected_features
    # Map back to feature names
    selected_feature_names = [feature_names[i] for i in range(
        len(feature_names)) if selected_features_mask[i]]

    return list(selected_feature_names)


def classification_read_optimal_features(all_log_paths, classification_method, measure_name, feature_portfolio, algorithm_portfolio, cv=5, scoring='accuracy'):
    cache_file_path = f"{globals.flask_app_path}/cache/optimal_features_lists/optimal_features_{classification_method}_{measure_name}.pk"
    try:
        optimal_features_list = load_cache_variable(cache_file_path)
    except Exception:
        print(
            f"optimal features list for {measure_name} does not exist yet, now computing")
        generate_cache_file(cache_file_path)
        optimal_features_list = compute_optimal_features(
            all_log_paths, classification_method, measure_name, feature_portfolio, algorithm_portfolio, cv=5, scoring='accuracy')
        store_cache_variable(optimal_features_list, cache_file_path)

        file_path = f"{globals.flask_app_path}/cache/optimal_features_lists/optimal_features_{classification_method}_{measure_name}.txt"
        with open(file_path, 'w') as file:
            for feature in optimal_features_list:
                file.write("%s\n" % feature)

        print("List written to file successfully.")

    return optimal_features_list


def classification_compute_optimal_features(all_log_paths, classification_method, measure_name, feature_portfolio, algorithm_portfolio, cv=5, scoring='accuracy'):
    """
    Selects the optimal set of features for accuracy using RFECV and returns the names of the selected features.

    :param estimator: A machine learning model that exposes the 'coef_' or 'feature_importances_' attribute.
    :param X: Feature matrix.
    :param y: Target vector.
    :param feature_names: List of feature names.
    :param cv: Number of cross-validation folds.
    :param scoring: Scoring metric, default is 'accuracy'.
    :return: A tuple containing the selector object, the transformed feature matrix, and the names of selected features.
    """

    # Create the RFECV object
    # Encode the target vector

    ret = compute_fitted_classifier(
        classification_method, measure_name, all_log_paths)
    clf = ret

    X = read_feature_matrix(all_log_paths, feature_portfolio)
    y = read_classification_target_vector(
        all_log_paths, measure_name, algorithm_portfolio)

    # Create the RFECV object
    print("creating RFECV object")
    rfecv = RFECV(estimator=clf, step=1,
                  cv=StratifiedKFold(cv), scoring=scoring)

    # Fit RFECV
    print("now starting fitting of RFECV")
    rfecv.fit(X, y)

    # Print the optimal number of features
    print(f"Optimal number of features: {rfecv.n_features_}")

    selected_features = [feature_portfolio[i]
                         for i in range(len(feature_portfolio)) if rfecv.support_[i]]

    return selected_features


if __name__ == "__main__":

    globals.algorithm_portfolio = [
        "alpha", "inductive", "heuristic", "split", "ILP"]
    feature_dict = get_total_feature_functions_dict()

    feature_list = list(feature_dict.keys())

    all_logs = gather_all_xes("../logs/testing") + gather_all_xes(
        "../logs/modified_eventlogs") + gather_all_xes("../logs/training")

    globals.selected_features = feature_list
    globals.measures_list = ["token_fitness", "token_precision",
                             "no_total_elements", "generalization", "pm4py_simplicity"]

    training_log_paths = get_all_ready_logs(
        all_logs, globals.selected_features, globals.algorithm_portfolio)
    init_given_parameters(training_log_paths, globals.algorithm_portfolio,
                          feature_list, globals.measures_list)

    for measure_name in globals.measures_list:
        input(compute_optimal_features(training_log_paths,
              "xgboost", measure_name, globals.selected_features))
