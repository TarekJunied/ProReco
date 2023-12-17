from utils import read_logs, read_models, read_model, read_log, load_cache_variable, store_cache_variable, generate_log_id, generate_cache_file,  read_log
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from features import read_feature_matrix, read_feature_vector, feature_no_events_total
from measures import read_target_entries, read_target_entry, read_classification_target_vector, read_measure_entry
from filehelper import gather_all_xes, split_file_path, get_all_ready_logs_multiple
from LogGenerator.log_generator import create_random_log
import multiprocessing
import globals
import random
import sys
import pm4py
import os


def fix_corrupt_cache():
    cache_folder = f"{globals.flask_app_path}/cache/"
    for folder_path, _, filenames in os.walk(cache_folder):
        for filename in filenames:
            if filename.endswith(".pkl"):
                file_path = os.path.join(folder_path, filename)

                try:
                    load_cache_variable(file_path)
                except Exception as e:
                    os.remove(file_path)
                    print(f"Error loading {file_path}: {e}")


def get_log_name(log_path):
    return split_file_path(log_path)["filename"]

# TODO: change util functions to try to read


def load_logs():
    training_log_paths = get_all_ready_logs_multiple(
        gather_all_xes("../logs/training"))
    testing_log_paths = get_all_ready_logs_multiple(
        gather_all_xes("../logs/testing"))

    for log_path in training_log_paths:
        log_name = get_log_name(log_path)
        globals.training_log_paths[log_path] = load_cache_variable(
            f"{globals.flask_app_path}/cache/logs/{log_name}.pkl")

    for log_path in testing_log_paths:
        log_name = get_log_name(log_path)
        globals.testing_log_paths[log_path] = load_cache_variable(
            f"{globals.flask_app_path}/cache/logs/{log_name}.pkl")


def load_measures():
    log_paths = list(globals.training_log_paths.keys()) + \
        list(globals.testing_log_paths.keys())

    for log_path in log_paths:
        for measure in globals.measures_list:
            for discovery_algorithm in globals.algorithm_portfolio:
                log_name = get_log_name(log_path)
                globals.measures[log_path, discovery_algorithm, measure] = load_cache_variable(
                    f"{globals.flask_app_path}/cache/measures/{discovery_algorithm}_{measure}_{log_name}.pkl")


def load_models():
    log_paths = list(globals.training_log_paths.keys()) + \
        list(globals.testing_log_paths.keys())
    for log_path in log_paths:
        for discovery_algorithm in globals.algorithm_portfolio:
            log_name = get_log_name(log_path)
            globals.models[log_path, discovery_algorithm] = load_cache_variable(
                f"{globals.flask_app_path}/cache/models/{discovery_algorithm}_{log_name}.pkl")


def load_features():
    log_paths = list(globals.training_log_paths.keys()) + \
        list(globals.testing_log_paths.keys())
    for log_path in log_paths:
        log_name = get_log_name(log_path)
        for feature in globals.selected_features:
            globals.features[log_path, feature] = load_cache_variable(
                f"{globals.flask_app_path}/cache/features/{feature}_{log_name}.pkl")


def init():
    load_logs()
    load_measures()
    load_models()
    load_features()


def init_training_logs(training_log_paths, list_of_measure_names):
    read_logs(training_log_paths)

    read_models(training_log_paths)

    x = read_feature_matrix(training_log_paths)

    for measure_name in list_of_measure_names:
        read_target_entries(training_log_paths, measure_name)


def init_real_life_logs(real_life_log_paths, list_of_measure_names):

    for log_path in real_life_log_paths:
        train_xes, test_xes = split_logpath(log_path)
        break_up_logpath(train_xes)
        break_up_logpath(test_xes)
        init_log(train_xes, list_of_measure_names)
        init_log(test_xes, list_of_measure_names)


def init_log(log_path):
    list_of_measure_names = globals.measures

    read_log(log_path)
    for discovery_algorithm in globals.algorithm_portfolio:
        read_model(log_path, discovery_algorithm)

    read_feature_vector(log_path)

    for measure in list_of_measure_names:
        for discovery_algorithm in globals.algorithm_portfolio:
            try:
                read_measure_entry(log_path, discovery_algorithm, measure)
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
        f"{globals.flask_app_path}/cache/logs/filtered_{log_path_filename}.pkl")

    store_cache_variable(filtered_log, cache_filepath)

    return filtered_log


def split_logpath(log_path, train_percentage=0.7):

    log_id = generate_log_id(log_path)

    train_log_filename = f"{log_id}_train"
    test_log_filename = f"{log_id}_test"

    train_xes_filepath = f"../logs/training/{train_log_filename}.xes"
    test_xes_filepath = f"../logs/testing/{test_log_filename}.xes"

    train_cache_filepath = generate_cache_file(
        f"{globals.flask_app_path}/cache/logs/{train_log_filename}.pkl")
    test_cache_filepath = generate_cache_file(
        f"{globals.flask_app_path}/cache/logs/{test_log_filename}.pkl")

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


def split_list_random_sizes(lst):
    min_size = 1000
    max_size = 2000
    sublists = []
    current_sublist = []

    while lst:
        size = random.randint(min_size, max_size)
        current_sublist = lst[:size]
        sublists.append(current_sublist)
        lst = lst[size:]

    return sublists


def create_and_init(index, mode):

    log_path = create_random_log(index, mode)

    init_log(log_path)

# Function to get the size of a file


def get_file_size(file_path):
    return os.path.getsize(file_path)


def get_file_size(file_path):
    return os.path.getsize(file_path)


def sort_files_by_size(file_paths):
    return sorted(file_paths, key=get_file_size)


def try_init_log(log_path):
    list_of_measure_names = globals.measures
    try:
        read_log(log_path)
    except Exception as e:
        print("Could not parse log")
        print(e)
    for discovery_algorithm in globals.algorithm_portfolio:
        try:
            read_model(log_path, discovery_algorithm)
        except Exception as e:
            print(
                f"Could not discover model for {discovery_algorithm} on {log_path}")
            print(e)

    try:
        read_feature_vector(log_path)
    except Exception as e:
        print("Couldn't compute feature vector")
        print(e)

    for measure in list_of_measure_names:
        for discovery_algorithm in globals.algorithm_portfolio:
            try:
                read_measure_entry(log_path, discovery_algorithm, measure)
            except Exception as e:
                print(
                    f"Could not compute measure {measure} on {discovery_algorithm}, {log_path}")
                print(e)


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    log_folder_paths = []

    # Check if at least one argument is provided
    if len(sys.argv) > 1:
        # sys.argv[1] is the first command line argument
        for i in range(1, len(sys.argv)):
            log_folder_paths += [sys.argv[i]]
    else:
        print("No input provided")
        sys.exit(-1)

    print("now startin init")
    print(log_folder_paths)
    logs_to_init = []
    for log_folder_path in log_folder_paths:
        logs_to_init += gather_all_xes(log_folder_path)

    logs_to_init = sort_files_by_size(logs_to_init)
    num_processes = 48

    pool = multiprocessing.Pool(processes=num_processes)

    print("now mapping pool")
    pool.map(try_init_log, logs_to_init)

    print("pool map done")
    pool.close()
    print("pool closed")
    pool.join()
    print("pool joined")

    print("done")
