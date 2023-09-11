import sys
from filehelper import gather_all_xes
from utils import read_logs,read_models,split_list
from features import read_feature_matrix
from measures import read_target_entries



if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    training_logsdir = "./LogGenerator/logs"

    training_log_paths = gather_all_xes("../logs/Process_Discovery_Contests/training")


    node_id = int(sys.argv[1])
    total_nodes = int(sys.argv[2])

    list_of_lists = split_list(training_log_paths, total_nodes)

    selected_logpaths = list_of_lists[node_id]


    print("CODE 23092002")    