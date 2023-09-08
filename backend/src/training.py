import sys
from filehelper import gather_all_xes
from utils import read_logs,read_models,split_list
from features import read_feature_matrix










if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    training_logsdir = "./LogGenerator/logs"

    training_log_paths = gather_all_xes(training_logsdir)


    node_id = int(sys.argv[1])
    total_nodes = int(sys.argv[2])

    list_of_lists = split_list(training_log_paths, total_nodes)

    selected_logpaths = list_of_lists[node_id]




    read_logs(selected_logpaths)

    read_models(selected_logpaths)

    x = read_feature_matrix(selected_logpaths)

    print("CODE 23092002")    