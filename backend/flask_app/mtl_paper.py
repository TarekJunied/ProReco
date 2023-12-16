import csv
import os
import copy
import pandas as pd
import globals
from tqdm import tqdm
from features import read_single_feature, read_feature_matrix
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from utils import get_log_name
from measures import read_target_entry, read_measure_entry
from filehelper import gather_all_xes, get_all_ready_logs, get_all_ready_logs_multiple
from recommender import classification_prediction_ranking, classification


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


def get_mtl_target_vector(all_log_paths):
    return 0


def do_mtl_evaluation_experiment(all_log_paths):
    X = pd.DataFrame(read_feature_matrix(all_log_paths),
                     columns=globals.selected_features)

    X.index = [get_log_name(log_path) for log_path in all_log_paths]
    label = pd.DataFrame(columns=["target"])
    i = 0
    for log_path in all_log_paths:
        label.loc[i] = [read_mtl_target_entry(log_path)]
        i += 1

    label['target'] = label['target'].astype('category')
    label_codes = label['target'].cat.codes


    for step in range(30):
    X_train, X_test, y_train, y_test = train_test_split(X, label, stratify=label, random_state=step)
    
    rf = RandomForestClassifier(random_state=step)
    rf.fit(X_train, y_train)

    result = rf.predict(X_test)
    result_df = pd.concat([result_df, pd.DataFrame([[rf.score(X_test, y_test), f1_score(y_test, result, average='macro')]])])

    result_df.columns = ["Acc", "F1-Score"]
    result_df["Metric"] = "Meta-Model"



if __name__ == "__main__":
    globals.algorithm_portfolio = [
        "alpha", "inductive", "heuristic"]
    # + "inductive_infrequent", "inductive_direct"

    log_paths = get_all_ready_logs_multiple(gather_all_xes("../logs/training"))
    algorithm_portfolio = copy.deepcopy(globals.algorithm_portfolio)

    do_mtl_evaluation_experiment(log_paths)
