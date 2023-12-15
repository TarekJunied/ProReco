import csv
import os
import copy
import globals
from tqdm import tqdm
from features import read_single_feature
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from utils import get_log_name
from measures import read_target_entry, read_measure_entry
from filehelper import gather_all_xes, get_all_ready_logs, get_all_ready_logs_multiple
from recommender import classification_prediction_ranking, classification


def actual_ranking(log_path, measure, ready_training):
    ret = []
    old_portfolio = copy.deepcopy(globals.algorithm_portfolio)
    for discovery_algorithm in old_portfolio:
        ret += [read_target_entry(log_path, measure)]
        globals.algorithm_portfolio.remove(discovery_algorithm)

    globals.algorithm_portfolio = copy.deepcopy(globals.algorithm_portfolio)
    return ret


def compute_mtl_algorith_ranking(log_path, discovery_algorithm, ready_training):
    rank_sum = 0
    for measure in ["token_fitness", "token_precision", "generalization", "pm4py_simplicity"]:
        input(actual_ranking(log_path, measure, ready_training))
        rank_measure = actual_ranking(
            log_path, measure, ready_training).index(discovery_algorithm) + 1
        rank_sum += rank_measure
    return rank_sum / 4


def read_mtl_target_entry(log_path, ready_training):
    cur_min_ranking = float("Inf")
    cur_best = None
    for discovery_algorithm in globals.algorithm_portfolio:
        cur_ranking = compute_mtl_algorith_ranking(
            log_path, discovery_algorithm, ready_training)
        if cur_ranking < cur_min_ranking:
            cur_min_ranking = cur_ranking
            cur_best = discovery_algorithm
    print(cur_min_ranking)
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


def create_csv_from_list(data, filepath):
    """
    data = [
    ['Name', 'Age', 'City'],
    ['John Doe', 25, 'New York'],
    ['Jane Smith', 30, 'San Francisco'],
    ['Bob Johnson', 22, 'Los Angeles']
    ]
    Args:
        look at above
    """
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header
        writer.writerow(data[0])

        # Write the remaining rows
        writer.writerows(data[1:])

        print(f'CSV file "{filepath}" has been created.')


def create_log_features_csv(log_paths, filepath):
    first_row = ["log"] + globals.selected_features
    data = [first_row]
    i = 1
    for log_path in log_paths:
        log_name = get_log_name(log_path)
        cur_row = [f"{log_name}"]
        for feature in globals.selected_features:
            cur_row += [read_single_feature(log_path, feature)]
        data += [cur_row]
        i += 1
    create_csv_from_list(data, filepath)


def translate_algorithm_naming(our_algorithm_name):
    if our_algorithm_name == "alpha":
        return "AM"
    elif our_algorithm_name == "heuristic":
        return "HM"
    elif our_algorithm_name == "inductive":
        return "IM"
    elif our_algorithm_name == "inductive_infrequent":
        return "IMf"
    elif our_algorithm_name == "inductive_direct":
        return "IMd"


def create_model_metrics_csv(log_paths, ready_training, filepath):
    first_row = ["log", "variant", "discovery_time", "fitness_time", "precision_time", "generalization_time", "simplicity_time", "perc_fit_traces", "average_trace_fitness", "log_fitness", "precision", "generalization", "simplicity"
                 ]
    data = [first_row]
    i = 1
    for log_path in log_paths:
        log_name = get_log_name(log_path)
        cur_row = [f"{log_name}"]
        for column in first_row:
            if column == "variant":
                target_entry = read_mtl_target_entry(log_path, ready_training)
                cur_row += [translate_algorithm_naming(target_entry)]
            elif column in ["discovery_time", "fitness_time", "precision_time", "generalization_time", "simplicity_time", "perc_fit_traces", "average_trace_fitness"]:
                cur_row += [0]
            elif column == "log_fitness":
                target_entry = read_mtl_target_entry(log_path, ready_training)
                cur_row += [read_measure_entry(log_path,
                                               target_entry, "token_fitness")]
            elif column == "precision":
                target_entry = read_mtl_target_entry(log_path, ready_training)
                cur_row += [read_measure_entry(log_path,
                                               target_entry, "token_precision")]
            elif column == "generalization":
                target_entry = read_mtl_target_entry(log_path, ready_training)
                cur_row += [read_measure_entry(log_path,
                                               target_entry, "token_generalization")]
            elif column == "simplicity":
                target_entry = read_mtl_target_entry(log_path, ready_training)
                cur_row += [read_measure_entry(log_path,
                                               target_entry, "simplicity")]

        data += [cur_row]
        i += 1
    create_csv_from_list(data, filepath)


if __name__ == "__main__":
    globals.algorithm_portfolio = ["alpha", "heuristic",
                                   "inductive"]

    # globals.algorithm_portfolio += ["inducitve_infrequent","inductive_direct"]

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

    ready_logs = get_all_ready_logs_multiple(
        gather_all_xes("../logs/training"))

    input(read_mtl_target_entry(ready_logs[0], ready_logs))
    input("hi")
    # create_log_features_csv(ready_logs,"./hi.csv")
