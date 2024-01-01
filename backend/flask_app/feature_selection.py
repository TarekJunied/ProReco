import pandas as pd
import concurrent.futures
import sys
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
from flask_app.features.mtl_features.mtl_feature_interface import get_mtl_feature_functions_dict
from flask_app.features.fig4pm_features.fig4pm_interface import get_fig4pm_feature_functions_dict
from classifiers import compute_fitted_classifier, read_fitted_classifier
from regressors import compute_fitted_regressor, read_fitted_regressor
from measures import read_classification_target_vector, read_regression_target_vector
from init import load_logs_into_main_memory, load_features_into_main_memory, load_measures_into_main_main_memory, fix_corrupt_cache, init_given_parameters
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.feature_selection import RFECV
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.model_selection import KFold, cross_val_score
from sklearn.base import clone
from sklearn.metrics import accuracy_score
from filehelper import split_file_path
from utils import generate_log_id, generate_cache_file, store_cache_variable, load_cache_variable, get_log_name


# Assuming X and y are your features and target variable


import pandas as pd


def top_n_correlated_features(log_paths, feature_portfolio, n):
    feature_matrix = read_feature_matrix(log_paths, feature_portfolio)
    # Convert the feature matrix to a DataFrame if it isn't one already
    df = pd.DataFrame(feature_matrix, columns=feature_portfolio)

    # Calculate the correlation matrix
    corr_matrix = df.corr()

    # Create a series to hold feature pairs and their correlations
    corr_series = (corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool_))
                   .stack()
                   .sort_values(ascending=False))
 # Extract indices of the top n correlated pairs
    top_pairs = corr_series.head(n).index

    # Extract unique feature names from the top pairs
    unique_features = set()
    for (feature1, feature2) in top_pairs:
        unique_features.add(feature1)
        unique_features.add(feature2)

    return list(unique_features)


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


def plot_feature_correlation(ready_logpaths, feature_portfolio, plot_title):
    X = read_feature_matrix(ready_logpaths, feature_portfolio)

    # Convert the numpy array 'X' to a DataFrame for easier manipulation
    feature_matrix = pd.DataFrame(X, columns=feature_portfolio)

    # Calculate the correlation matrix
    corr = feature_matrix.corr()

    # Set up the matplotlib figure with a suitable size for 10 features
    plt.figure(figsize=(20, 20))  # Adjusted for 10 features

    # Draw the heatmap
    sns.heatmap(corr,
                xticklabels=corr.columns,
                yticklabels=corr.columns,
                cmap='coolwarm',    # You can choose a different colormap
                annot=True,         # Set to True if you want to see the correlation values
                linewidths=.5)

    # Adding labels and title for clarity
    plt.title('Feature Correlations', fontsize=20)  # Adjusted font size
    plt.xlabel('Features', fontsize=20)             # Adjusted font size
    plt.ylabel('Features', fontsize=20)             # Adjusted font size

    # Adjusting tick labels for readability
    plt.xticks(rotation=45, fontsize=12)  # Adjusted for better readability
    plt.yticks(rotation=0, fontsize=12)   # Adjusted for better readability

    # Save the plot
    plt.savefig(
        f"../evaluation/feature_correlation/{plot_title}_correlation.png")


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
        optimal_features_list = classification_compute_optimal_features(
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


def regression_select_k_best_features(log_paths, model_portfolio, feature_portfolio, target_variable, k=100):
    X_train = read_feature_matrix(log_paths, feature_portfolio)
    y_train = read_regression_target_vector(
        log_paths, target_variable, model_portfolio)
    selector_kbest = SelectKBest(f_regression, k=k)

    # Fit the selector to the data
    X_kbest_selected = selector_kbest.fit_transform(X_train, y_train)

    # Now you can use get_support() as the selector is fitted
    selected_features_mask = selector_kbest.get_support()

    feature_names = globals.selected_features
    # Map back to feature names
    selected_feature_names = [feature_names[i] for i in range(
        len(feature_names)) if selected_features_mask[i]]

    return list(selected_feature_names)


def regression_read_optimal_features(all_log_paths, regression_method, discovery_algorithm, measure_name, feature_portfolio, cv=5, scoring='r2'):
    cache_file_path = f"{globals.flask_app_path}/cache/optimal_features_lists/regression/{regression_method}/optimal_features_{discovery_algorithm}_{measure_name}.pk"
    try:
        optimal_features_list = load_cache_variable(cache_file_path)
    except Exception:
        print(
            f"Optimal features list for {regression_method} {discovery_algorithm} {measure_name} does not exist yet, now computing")
        optimal_features_list = regression_compute_optimal_features(
            all_log_paths, regression_method, discovery_algorithm, measure_name, feature_portfolio, cv=cv, scoring='r2')
        generate_cache_file(cache_file_path)
        store_cache_variable(optimal_features_list, cache_file_path)

        file_path = f"{globals.flask_app_path}/cache/optimal_features_lists/regression/{regression_method}/optimal_features_{discovery_algorithm}_{measure_name}.txt"
        with open(file_path, 'w') as file:
            for feature in optimal_features_list:
                file.write("%s\n" % feature)

        print("List written to file successfully.")

    return optimal_features_list


def regression_compute_optimal_features(all_log_paths, regression_method, discovery_algorithm, measure_name, feature_portfolio, cv=5, scoring='r2'):
    """
    Selects the optimal set of features for R2 (or other scoring) using RFECV and returns the names of the selected features.

    :param estimator: A regression model that exposes 'coef_' or 'feature_importances_' attributes.
    :param X: Feature matrix.
    :param y: Target vector.
    :param feature_names: List of feature names.
    :param cv: Number of cross-validation folds.
    :param scoring: Scoring metric, default is 'r2'.
    :return: A list containing the names of selected features.
    """

    # Create the RFE object
    ret = compute_fitted_regressor(
        regression_method, discovery_algorithm, measure_name, all_log_paths, feature_portfolio)
    reg = ret

    X = read_feature_matrix(all_log_paths, feature_portfolio)
    y = read_regression_target_vector(
        all_log_paths, discovery_algorithm, measure_name)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # Create the RFECV object
    print("Creating RFECV object")
    rfecv = RFECV(estimator=reg, step=1,
                  cv=KFold(cv), scoring=scoring)

    # Fit RFECV
    print("Now starting fitting of RFECV")
    rfecv.fit(X_train, y_train)

    # Print the optimal number of features
    print(f"Optimal number of features: {rfecv.n_features_}")

    selected_features = [feature_portfolio[i]
                         for i in range(len(feature_portfolio)) if rfecv.support_[i]]

    return selected_features


def clear_regression_optimal_features():
    cache_file_path = f"{globals.flask_app_path}/cache/optimal_features_lists/"
    for file_name in os.listdir(cache_file_path):
        # Construct full file path
        file_path = os.path.join(cache_file_path, file_name)
        # Check if the current object is a file and has "regression" in its name
        if os.path.isfile(file_path) and 'regression' in file_name:
            # Delete the file
            os.remove(file_path)
            print(f"Deleted {file_path}")


def remove_substrings(original_string, substrings):
    substrings = sorted(substrings, key=len, reverse=True)
    for substring in substrings:
        original_string = original_string.replace(substring, "")
    return original_string


def process_combination(args):
    regression_method, discovery_algorithm, measure_name, training_log_paths, selected_features = args
    try:
        regression_read_optimal_features(
            training_log_paths, regression_method, discovery_algorithm, measure_name, selected_features)
    except Exception as e:
        return (e, "next ?")  # or handle it in some way


if __name__ == "__main__":

    feature_dict = get_total_feature_functions_dict()
    feature_list = list(feature_dict.keys())

    globals.selected_features = feature_list
    all_logs = gather_all_xes("../logs/testing") + gather_all_xes(
        "../logs/modified_eventlogs") + gather_all_xes("../logs/training")

    training_log_paths = get_all_ready_logs(
        all_logs, globals.selected_features, globals.algorithm_portfolio, globals.measures_list)

    regression_method = sys.argv[1]
    discovery_algorithm = sys.argv[2]
    measure_name = sys.argv[3]

    init_given_parameters(training_log_paths, [
                          discovery_algorithm], globals.selected_features, [measure_name])

    regression_read_optimal_features(
        training_log_paths, regression_method, discovery_algorithm, measure_name, globals.selected_features)
