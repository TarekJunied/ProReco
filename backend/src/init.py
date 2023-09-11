from utils import read_logs, read_models,read_model,read_log
from features import read_feature_matrix,read_feature_vector
from measures import read_target_entries, read_target_entry


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
    read_log(log_path)

    read_model(log_path)

    read_feature_vector(log_path)

    for measure_name in list_of_measure_names:
        read_target_entry(log_path,measure_name)

