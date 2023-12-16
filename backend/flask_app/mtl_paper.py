import numpy as np
import os
import copy
import pandas as pd
import globals
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score
from features import read_single_feature, read_feature_matrix
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from utils import get_log_name, load_cache_variable, store_cache_variable
from measures import read_target_entry, read_measure_entry
from filehelper import gather_all_xes, get_all_ready_logs, get_all_ready_logs_multiple
from recommender import classification_prediction_ranking, classification


def read_fitted_classifier(classification_method,  x_train, y_train):
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

    return clf


def actual_ranking(log_path, measure):
    ret = []
    portfolio_copy = copy.deepcopy(globals.algorithm_portfolio)
    n = len(portfolio_copy)
    for _ in range(n):
        target = read_target_entry(log_path, measure, portfolio_copy)
        ret += [target]
        portfolio_copy.remove(target)

    return ret


def compute_mtl_algorith_ranking(log_path, discovery_algorithm):
    rank_sum = 0
    for measure in ["token_fitness", "token_precision", "generalization", "pm4py_simplicity"]:
        rank_measure = actual_ranking(
            log_path, measure).index(discovery_algorithm) + 1
        rank_sum += rank_measure
    return rank_sum / 4


def read_mtl_target_entry(log_path):
    cur_min_ranking = float("Inf")
    cur_best = None
    for discovery_algorithm in globals.algorithm_portfolio:
        cur_ranking = compute_mtl_algorith_ranking(
            log_path, discovery_algorithm)
        if cur_ranking < cur_min_ranking:
            cur_min_ranking = cur_ranking
            cur_best = discovery_algorithm
    return cur_best


def ungz_logpaths_folder(event_logs_path):

    event_logs_path = "../logs/process_meta_learning_logs/event_logs"
    for f in tqdm(os.listdir(event_logs_path)):
        log = xes_importer.apply(
            f"{event_logs_path}/{f}", parameters={"show_progress_bar": False}
        )
        f_name = f.split(".gz")[0]
        xes_exporter.apply(
            log, f"{event_logs_path}/{f_name}", parameters={"show_progress_bar": False}
        )
        os.remove(f"{event_logs_path}/{f}")


def read_mtl_target_vector(all_log_paths):
    label = pd.DataFrame(columns=["target"])
    i = 0
    for log_path in all_log_paths:
        label.loc[i] = [read_mtl_target_entry(log_path)]
        i += 1

    label['target'] = label['target'].astype('category')
    return label['target'].cat.codes


def get_mtl_X_feature_matrix(ready_logs):
    X = pd.DataFrame(read_feature_matrix(ready_logs),
                     columns=globals.selected_features)

    X.index = [get_log_name(log_path) for log_path in ready_logs]
    return X


def do_mtl_classification_evaluation_experiment(X, label, classification_method):
    result_df = pd.DataFrame()
    for step in range(30):
        X_train, X_test, y_train, y_test = train_test_split(
            X, label, stratify=label, random_state=step)

        clf = read_fitted_classifier(classification_method, X_train, y_train)
        result = clf.predict(X_test)
        result_df = pd.concat([result_df, pd.DataFrame(
            [[clf.score(X_test, y_test), f1_score(y_test, result, average='macro')]])])

    result_df.columns = ["Acc", "F1-Score"]
    result_df["Metric"] = "Meta-Model"
    return result_df


def do_mtl_random_approach_experiment(X, label):
    result_df_rnd = pd.DataFrame()
    for step in range(30):
        X_train, X_test, y_train, y_test = train_test_split(
            X, label, stratify=label, random_state=step)

        random_y = np.random.randint(
            len(label.unique()), size=(1, len(y_test)))
        result_df_rnd = pd.concat([result_df_rnd, pd.DataFrame([[accuracy_score(
            y_test.values, random_y[0]), f1_score(y_test.values, random_y[0], average='macro')]])])

    result_df_rnd.columns = ["Acc", "F1-Score"]
    result_df_rnd["Metric"] = "Random"
    return result_df_rnd


def do_mtl_majority_experiment(X, label):
    # Majority approach (AM)
    result_df_maj = pd.DataFrame()
    for step in range(30):
        X_train, X_test, y_train, y_test = train_test_split(
            X, label, stratify=label, random_state=step)

        majority_y = np.zeros(len(y_test))
        result_df_maj = pd.concat([result_df_maj, pd.DataFrame([[accuracy_score(
            y_test.values, majority_y), f1_score(y_test.values, majority_y, average='macro')]])])

    result_df_maj.columns = ["Acc", "F1-Score"]
    result_df_maj["Metric"] = "Majority (AM)"
    return result_df_maj


def do_mtl_evaluation_experiment(all_log_paths, classification_method):
    X = get_mtl_X_feature_matrix(all_log_paths)
    label = read_mtl_target_vector(all_log_paths)

    result_df = do_mtl_classification_evaluation_experiment(
        X, label, classification_method)
    result_df_rnd = do_mtl_random_approach_experiment(X, label)
    result_df_maj = do_mtl_majority_experiment(X, label)

    dataset_for_seaborn = pd.melt(
        pd.concat([result_df, result_df_maj, result_df_rnd]), id_vars="Metric")
    dataset_for_seaborn.columns = ["Method", "Metric", "Performance"]
    print(dataset_for_seaborn)

    plt.figure(figsize=(5, 4))
    ax = sns.boxplot(x="Method", y="Performance", hue="Metric",
                     data=dataset_for_seaborn, palette="YlGnBu")
    ax.yaxis.grid(True)
    # Save the plot to a file.
    # You can change the file name and extension as needed.
    plt.savefig(f"./{classification_method}_boxplot.png")

    # Optional: Close the figure to free up memory.
    plt.close()


if __name__ == "__main__":
    globals.algorithm_portfolio = [
        "alpha", "inductive", "heuristic"]
    # + "inductive_infrequent", "inductive_direct"

    log_paths = get_all_ready_logs_multiple(gather_all_xes("../logs/training"))
    algorithm_portfolio = copy.deepcopy(globals.algorithm_portfolio)
    for classification_method in globals.classification_methods:
        do_mtl_evaluation_experiment(log_paths, classification_method)
