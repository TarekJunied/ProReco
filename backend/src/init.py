from utils import read_logs, read_models,read_model,read_log,filter_log_path,load_cache_variable,store_cache_variable,generate_log_id, generate_cache_file
from features import read_feature_matrix,read_feature_vector
from measures import read_target_entries, read_target_entry
from filehelper import gather_all_xes,select_smallest_k_logs
import globals
import multiprocessing
import sys
import pm4py

def init(training_log_paths,testing_log_paths,list_of_measure_names):

    init_training_logs(training_log_paths,list_of_measure_names)

def init_training_logs(training_log_paths,list_of_measure_names):
    read_logs(training_log_paths)

    read_models(training_log_paths)

    x = read_feature_matrix(training_log_paths)

    for measure_name in list_of_measure_names:
        read_target_entries(training_log_paths,measure_name)

def init_testing_logs(testing_log_paths, list_of_measure_names):
    #TODO: maybe do filtering here first

    read_logs(testing_log_paths)

    read_models(testing_log_paths)

    for log_path in testing_log_paths:
        read_feature_vector(log_path)

    y = [None]*len(testing_log_paths)
    for i in range(len(testing_log_paths)):
        for measure_name in list_of_measure_names:
            read_target_entry(testing_log_paths[i],measure_name)

def init_log(log_path,list_of_measure_names):
    try:
        filter_log_path(log_path,10)

        read_log(log_path)
        for discovery_algorithm in globals.algorithm_portfolio:
            read_model(log_path,discovery_algorithm)


        read_feature_vector(log_path)

        for measure_name in list_of_measure_names:
            read_target_entry(log_path,measure_name)
    except Exception as e:
        print(e)



def split_logpath(log_path, train_percentage):

    log = read_log(log_path)

    log_id = generate_log_id(log_path)

    train_log, test_log = pm4py.split_train_test(log, train_percentage)

    train_log_filename = f"{log_id}_train"
    test_log_filename = f"{log_id}_test"

    pm4py.write.write_xes(train_log,f"../logs/training/{train_log_filename}.xes")
    pm4py.write.write_xes(test_log,f"../logs/testing/{test_log_filename}.xes")

    train_cache_filepath = generate_cache_file(f"./cache/logs/{train_log_filename}.pkl")
    test_cache_filepath = generate_cache_file(f"./cache/logs/{test_log_filename}.pkl")

    store_cache_variable(train_log,train_cache_filepath)
    store_cache_variable(test_log,test_cache_filepath)

    return train_log,test_log




if __name__ == "__main__":
    sys.setrecursionlimit(5000)
    #num_cores = multiprocessing.cpu_count()
    #pool = multiprocessing.Pool(processes=num_cores)
    

    training_log_paths = gather_all_xes("./LogGenerator/logs")
    reallife_logpaths = gather_all_xes("../logs/real_life_logs")
    proc_disc = gather_all_xes("../logs/Process_Discovery_Contests")

    for log_path in reallife_logpaths:
        split_logpath(log_path, 0.7)

    
    