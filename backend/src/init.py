from utils import read_logs, read_models, read_model, read_log, load_cache_variable, store_cache_variable, generate_log_id, generate_cache_file, split_file_path, read_log
from features import read_feature_matrix, read_feature_vector, feature_no_distinct_traces
from measures import read_target_entries, read_target_entry, read_target_vector
from filehelper import gather_all_xes, select_smallest_k_logs
import globals
import math
import multiprocessing
import sys
import pm4py


def init(training_log_paths, testing_log_paths, list_of_measure_names):

    init_training_logs(training_log_paths, list_of_measure_names)


def init_training_logs(training_log_paths, list_of_measure_names):
    read_logs(training_log_paths)

    read_models(training_log_paths)

    x = read_feature_matrix(training_log_paths)

    for measure_name in list_of_measure_names:
        read_target_entries(training_log_paths, measure_name)


def init_testing_logs(testing_log_paths, list_of_measure_names):
    # TODO: maybe do filtering here first

    read_logs(testing_log_paths)

    read_models(testing_log_paths)

    for log_path in testing_log_paths:
        read_feature_vector(log_path)

    y = [None]*len(testing_log_paths)
    for i in range(len(testing_log_paths)):
        for measure_name in list_of_measure_names:
            read_target_entry(testing_log_paths[i], measure_name)


def init_log(log_path, list_of_measure_names):
    try:

        read_log(log_path)
        for discovery_algorithm in globals.algorithm_portfolio:
            read_model(log_path, discovery_algorithm)

        read_feature_vector(log_path)

        for measure_name in list_of_measure_names:
            read_target_entry(log_path, measure_name)
    except Exception as e:
        print(e)


def keep_top_percentage_traces(log_path, top_k):

    # no_traces = feature_no_distinct_traces(log_path)

    # k = math.ceil(no_traces*percentage)

    unfiltered_log = read_log(log_path)

    filtered_log = pm4py.filtering.filter_variants_top_k(unfiltered_log, top_k)

    split_dic = split_file_path(log_path)

    log_path_dir = split_dic["directory"]

    log_path_filename = split_dic["filename"]

    pm4py.write.write_xes(
        filtered_log, f"{log_path_dir}/filtered_{log_path_filename}.xes")

    cache_filepath = generate_cache_file(
        f"./cache/logs/filtered_{log_path_filename}.pkl")

    store_cache_variable(filtered_log, cache_filepath)

    return filtered_log


def split_logpath(log_path, train_percentage=0.7):

    log_id = generate_log_id(log_path)

    train_log_filename = f"{log_id}_train"
    test_log_filename = f"{log_id}_test"

    train_xes_filepath = f"../logs/training/{train_log_filename}.xes"
    test_xes_filepath = f"../logs/testing/{test_log_filename}.xes"

    train_cache_filepath = generate_cache_file(
        f"./cache/logs/{train_log_filename}.pkl")
    test_cache_filepath = generate_cache_file(
        f"./cache/logs/{test_log_filename}.pkl")

    try:
        train_log = read_log(train_cache_filepath)
        test_log = read_log(test_cache_filepath)
        return train_xes_filepath, test_xes_filepath
    except Exception:
        log = read_log(log_path)
        print("No cache file existing for split logs. Now splitting logs.")

        train_log, test_log = pm4py.split_train_test(log, train_percentage)

        pm4py.write.write_xes(train_log, train_xes_filepath)
        pm4py.write.write_xes(test_log, test_xes_filepath)

        store_cache_variable(train_log, train_cache_filepath)
        store_cache_variable(test_log, test_cache_filepath)

    return train_xes_filepath, test_xes_filepath


if __name__ == "__main__":
    sys.setrecursionlimit(5000)

    training_log_paths = gather_all_xes("../logs/training")
    testing_log_paths = gather_all_xes("../logs/testing")
    reallife_logpaths = gather_all_xes("../logs/real_life_logs")
    proc_disc = gather_all_xes("../logs/Process_Discovery_Contests")

    selected_measures = ["node_arc_degree", "no_total_elements",
                         "used_memory", "pm4py_simplicity", "runtime"]

    # init_training_logs(training_log_paths, selected_measures)
    init_testing_logs(testing_log_paths, selected_measures)
