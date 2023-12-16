# import shap
import matplotlib.pyplot as plt
import pandas as pd
import globals
import numpy as np
import subprocess
import os
import pm4py
from utils import read_logs, read_models,  get_all_ready_logs
from filehelper import gather_all_xes, get_all_ready_logs, get_all_ready_logs_multiple
from features import read_feature_matrix, read_feature_vector, feature_no_total_traces, space_out_feature_vector_string
from measures import read_measure_entry, read_regression_target_vector
from init import *
from autofolio_interface import autofolio_classification
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from lime import lime_tabular
from sklearn.tree import plot_tree


def read_multiobjective_graph(log_path, ready_training, measure_weight_dict, regression_method="linear_regression"):
    predicted_alg_values = {}
    relevant_measures = [key for key,
                         value in measure_weight_dict.items() if value > 0]
    predicted_algorithm_vectors = {algorithm: []
                                   for algorithm in globals.algorithm_portfolio}
    actual_algorithm_vectors = {algorithm: []
                                for algorithm in globals.algorithm_portfolio}

    for discovery_algorithm in globals.algorithm_portfolio:
        for measure_name in relevant_measures:
            predicted_value = regression(
                log_path, regression_method, measure_name, discovery_algorithm, ready_training)
            actual_value = read_measure_entry(
                log_path, discovery_algorithm, measure_name)
            predicted_alg_values[discovery_algorithm,
                                 measure_name] = predicted_value
            predicted_algorithm_vectors[discovery_algorithm].append(
                predicted_value)
            actual_algorithm_vectors[discovery_algorithm].append(actual_value)

    n = len(globals.algorithm_portfolio)
    predicted_dominated = set()
    actual_dominated = set()
    for i in range(n):
        for j in range(n):
            algo_i = globals.algorithm_portfolio[i]
            algo_j = globals.algorithm_portfolio[j]
            if algo_i_dominates_algo_j(predicted_algorithm_vectors[algo_i], predicted_algorithm_vectors[algo_j], relevant_measures):
                predicted_dominated.add(algo_j)
            if algo_i_dominates_algo_j(actual_algorithm_vectors[algo_i], actual_algorithm_vectors[algo_j], relevant_measures):
                actual_dominated.add(algo_j)

    print(f"predicted dominated algos {predicted_dominated}")
    print(f"acutal dominated algos {actual_dominated}")

    m = max(len(predicted_dominated), len(actual_dominated))
    u = len(predicted_dominated.intersection(actual_dominated))

    return u/m


def algo_i_dominates_algo_j(algo_i_value_vector, algo_j_value_vector, relevant_measures):
    i_dominates_j = True
    k = 0
    for measure in relevant_measures:
        if globals.measures_kind[measure] == "max":
            if algo_i_value_vector[k] <= algo_j_value_vector[k]:
                i_dominates_j = False
            elif globals.measures_kind[measure] == "min":
                if algo_i_value_vector[k] >= algo_j_value_vector[k]:
                    i_dominates_j = False
                else:
                    print("fuck")
                k += 1
    return i_dominates_j


def read_fitted_classifier(classification_method, measure_name, ready_training):
    classifier_filepath = f"./classifiers/{measure_name}_{classification_method}.pkl"
    try:
        clf = load_cache_variable(classifier_filepath)
    except Exception:
        print("Classifier doesn't exist yet. Computing classifier now")

        x_train = read_feature_matrix(ready_training)

        y_train = read_classification_target_vector(
            ready_training, measure_name)

        if classification_method == "decision_tree":
            clf = DecisionTreeClassifier()
        elif classification_method == "knn":
            clf = KNeighborsClassifier(n_neighbors=9)
        elif classification_method == "svm":
            clf = SVC(probability=True)
        elif classification_method == "random_forest":
            clf = RandomForestClassifier()
        elif classification_method == "logistic_regression":
            clf = LogisticRegression()
        elif classification_method == "gradient_boosting":
            clf = GradientBoostingClassifier(n_estimators=100)

        else:
            raise ValueError(
                f"Invalid classification method: {classification_method}")

        clf = clf.fit(x_train, y_train)

        store_cache_variable(clf, classifier_filepath)

    return clf


def read_fitted_regressor(regression_method, measure_name, discovery_algorithm, ready_training):
    regressor_filepath = f"./regressors/{regression_method}/{discovery_algorithm}_{measure_name}.pkl"

    try:
        reg = load_cache_variable(regressor_filepath)
    except Exception:
        print("Regressor doesn't exist yet. Computing regressor now")

        x_train = read_feature_matrix(ready_training)
        y_train = read_regression_target_vector(
            ready_training, discovery_algorithm, measure_name)

        if regression_method == "linear_regression":
            reg = LinearRegression()
        elif regression_method == "ridge_regression":
            reg = Ridge(alpha=1.0)
        elif regression_method == "lasso_regression":
            reg = Lasso(alpha=1.0)
        elif regression_method == "decision_tree":
            reg = DecisionTreeRegressor()
        elif regression_method == "random_forest":
            reg = RandomForestRegressor()
        elif regression_method == "gradient_boosting":
            reg = GradientBoostingRegressor(n_estimators=100)
        elif regression_method == "svm":
            reg = SVR()
        elif regression_method == "knn":
            reg = KNeighborsRegressor(n_neighbors=5)
        elif regression_method == "mlp":
            reg = MLPRegressor(hidden_layer_sizes=(100,), max_iter=500)
        else:
            raise ValueError(f"Invalid regression method: {regression_method}")

        reg = reg.fit(x_train, y_train)
        store_cache_variable(reg, regressor_filepath)

    return reg


def classification_prediction_ranking(log_path, classification_method, measure_name, ready_training):
    if classification_method == "autofolio":
        print("We don't support autofolio for this.")
        return

    clf = read_fitted_classifier(
        classification_method, measure_name, ready_training)

    # Check if the classifier has the predict_proba method
    if hasattr(clf, 'predict_proba'):
        # Read the feature vector from the log path
        feature_vector = read_feature_vector(log_path)

        # Get probability estimates for each class
        probabilities = clf.predict_proba(feature_vector)[0]

        # Get class labels
        classes = clf.classes_

        # Pair each probability with its corresponding class label
        probability_class_pairs = list(zip(probabilities, classes))

        # Sort the pairs in descending order of probability
        sorted_pairs = sorted(probability_class_pairs,
                              reverse=True, key=lambda pair: pair[0])

        # Extract the class labels in sorted order to get the ranking
        ranked_predictions = [pair[1] for pair in sorted_pairs]

        # Return the ranked predictions
        algos_left = set(globals.algorithm_portfolio) - set(ranked_predictions)
        return ranked_predictions + list(algos_left)
    else:
        print("This classifier does not support probability predictions.")
        return None


# TODO: tailor this again to backend
def classification(log_path, classification_method, measure_name, ready_training):
    if classification_method == "autofolio":
        return autofolio_classification(log_path, ready_training, measure_name)

    clf = read_fitted_classifier(
        classification_method, measure_name, ready_training)

    predictions = clf.predict(read_feature_vector(log_path))

    return predictions[0]

# TODO: tailor this again to backend


def regression(log_path, regression_method, measure_name, discovery_algorithm, ready_training):

    reg = read_fitted_regressor(
        regression_method, measure_name, discovery_algorithm, ready_training)

    prediction = reg.predict(read_feature_vector(log_path))

    return prediction[0]


def ranking_classification(log_path, classification_method, measure_name):
    if classification_method == "autofolio":
        return autofolio_classification(log_path, measure_name)

    clf = read_fitted_classifier(classification_method, measure_name, [])

    # Get probability estimates for each class
    proba = clf.predict_proba(read_feature_vector(log_path))

    # Assuming you want to get the rankings for each instance in X_test
    # argsort gives the indices that would sort an array in ascending order

    class_labels = clf.classes_

    ranking = np.argsort(-proba, axis=1)

    sorted_class_names = class_labels[ranking]

    class_ranking_array = [sorted_class_names[:, i][0]
                           for i in range(sorted_class_names.shape[1])]

    for algo in globals.algorithm_portfolio:
        if algo not in class_ranking_array:
            class_ranking_array += [algo]
    return class_ranking_array


def predict_regression(log_path, measure_name, ready_training, regression_method="linear_regression"):
    predicted_values = {}
    for discovery_algorithm in globals.algorithm_portfolio:
        predicted_values[discovery_algorithm] = regression(
            log_path, regression_method, measure_name, discovery_algorithm, ready_training)

    if globals.measures_kind[measure_name] == "max":
        ret = max(predicted_values, key=predicted_values.get)
    elif globals.measures_kind[measure_name] == "min":
        ret = min(predicted_values, key=predicted_values.get)
    else:
        print("Invalid kind of measures")
        input(measure_name)

        ret = None
    return ret


def final_prediction(log_path, measure_weight):
    """returns the predicted rankings
    1st place ILP => ret["ILP"] = 1
    Args:
        log_path: _description_
        measure_weight: _description_

    Returns:
        _description_
    """
    max_measure = max(measure_weight, key=lambda k: measure_weight[k])
    class_ranking_array = ranking_classification(
        log_path, "gradient_boosting", max_measure)
    ret = {}
    i = 1
    for class_label in class_ranking_array:
        ret[class_label] = i
        i += 1
    return ret


def measure_score(log_path, discovery_algorithm, measure):
    rank_list = {}
    for disco_algorithm in globals.algorithm_portfolio:
        rank_list[disco_algorithm] = read_measure_entry(
            log_path, disco_algorithm, measure)

    if str(globals.measures[measure]) == "min":
        sorted_items = sorted(
            rank_list.items(), reverse=True, key=lambda item: item[1])
    elif str(globals.measures[measure]) == "max":
        sorted_items = sorted(
            rank_list.items(), reverse=False, key=lambda item: item[1])
    else:
        print(globals.measures[measure] == "min")
    sorted_keys_list = [item[0] for item in sorted_items]
    return sorted_keys_list.index(discovery_algorithm) + 1


def list_files_with_sizes(file_paths):
    # Create a list to store file details
    file_details = []

    # Iterate over each file path
    for file_path in file_paths:
        # Get file size in bytes
        file_size = os.path.getsize(file_path)

        # Append file details to the list
        file_details.append((file_path, file_size))

    # Sort the list based on file size in descending order
    file_details.sort(key=lambda x: x[1], reverse=True)

    # Print the sorted file details
    for file_path, file_size in file_details:
        print(f"{file_path}: {file_size} bytes")


def read_shap_explainer(classification_method, x_train):
    cache_file_path = f"./cache/explainers/{classification_method}.pkl"
    try:
        explainer = load_cache_variable(cache_file_path)
    except Exception as e:

        clf = read_fitted_classifier(
            classification_method, chosen_measure, ready_training)

        if classification_method == "decision_tree" or classification_method == "random_forest":
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


def create_shap_graph(ready_training, ready_testing, classification_method, chosen_measure):
    x_test = read_feature_matrix(ready_testing)
    x_train = read_feature_matrix(ready_training)

    x_test = pd.DataFrame(x_test, columns=globals.selected_features)
    x_train = pd.DataFrame(x_train, columns=globals.selected_features)

    explainer = read_shap_explainer(classification_method, x_train)

    shap_values = explainer.shap_values(x_test)

    plt.clf()

    # Plot the SHAP summary plot
    shap.summary_plot(
        shap_values[1], x_test, feature_names=globals.selected_features, show=False)

    # Save the plot
    storage_dir = "../evaluation/shap"

    plt.savefig(
        f'{storage_dir}/{classification_method}_{chosen_measure}_shap_summary_plot.png')
    plt.show()


def create_lime_graph(measure_name):

    ready_training = get_all_ready_logs(
        gather_all_xes("../logs/training"), measure_name)
    ready_testing = get_all_ready_logs(
        gather_all_xes("../logs/testing"), measure_name)

    # Assume 'model' is your scikit-learn classifier
    x_test = read_feature_matrix(ready_testing)
    x_train = read_feature_matrix(ready_training)

    # x_test = pd.DataFrame(x_test, columns=globals.selected_features)
    # x_train = pd.DataFrame(x_train, columns=globals.selected_features)
    def custom_model_predict(x): return classification(
        x, "autofolio", measure_name, ready_training)

    # Assume 'X_train' is your training data
    explainer = lime_tabular.LimeTabularExplainer(
        x_train, mode="classification")

    input("hji")
    # Assume 'X_test[i]' is the instance you want to explain
    explanation = explainer.explain_instance(read_feature_vector(
        ready_testing[0]).values.reshape(1, -1), custom_model_predict)

    # Save the explanation plot as a PNG file
    explanation.save_to_file('lime_explanation_plot.png')


if __name__ == "__main__":
    # shap.initjs()
    globals.algorithm_portfolio = ["alpha", "heuristic",
                                   "inductive", "ILP", "split"]

    globals.selected_features = ["no_distinct_traces", "no_total_traces", "avg_trace_length", "avg_event_repetition_intra_trace",
                                 "no_distinct_events", "no_events_total", "no_distinct_start", "no_distinct_end", "density", "length_one_loops", "total_no_activities", "percentage_concurrency", "percentage_sequence",
                                 "dfg_mean_variable_degree",
                                 "dfg_variation_coefficient_variable_degree",
                                 "dfg_min_variable_degree",
                                 "dfg_max_variable_degree",
                                 "dfg_entropy_variable_degree",
                                 "dfg_wcc_min",
                                 "dfg_wcc_max",
                                 ]

    ready_training = get_all_ready_logs_multiple(
        gather_all_xes("../logs/training"))
    ready_testing = get_all_ready_logs_multiple(
        gather_all_xes("../logs/testing"))
    measure_weight_dict = {}
    for measure in globals.measures_list:
        measure_weight_dict[measure] = 0

    measure_weight_dict["token_fitness"] = 1
    measure_weight_dict["token_precision"] = 1
    # measure_weight_dict["generalization"] = 1
    # measure_weight_dict["pm4py_simplicity"] = 1

    sum = 0
    for log_path in ready_testing:
        sum += read_multiobjective_graph(log_path,
                                         ready_training, measure_weight_dict)

    input(sum/len(ready_testing))
