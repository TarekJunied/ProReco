import pm4py
import time
import pickle
from filehelper import gather_all_xes
from globals import logs, models, runtime


def print_distinct_traces(log_path):
    log = read_log(log_path)
    variants = pm4py.stats.get_variants(log)
    trace_variants = list(variants.keys())

    for trace in trace_variants:
        print(trace)


def read_model(log_path, discovery_algorithm):
    if (log_path, discovery_algorithm) not in models:
        log = read_log(log_path)
        start_time = time.time()
        if discovery_algorithm == "alpha":
            net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(
                log)
            models[log_path, discovery_algorithm] = (
                net, initial_marking, final_marking)

        elif discovery_algorithm == "heuristic":
            net, initial_marking, final_marking = pm4py.discover_petri_net_heuristics(
                log)
            models[log_path, discovery_algorithm] = (
                net, initial_marking, final_marking)
        elif discovery_algorithm == "ILP":
            net, initial_marking, final_marking = pm4py.discover_petri_net_ilp(
                log)
            models[log_path, discovery_algorithm] = (
                net, initial_marking, final_marking)

        elif discovery_algorithm == "inductive":
            net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(
                log)
            models[log_path, discovery_algorithm] = (
                net, initial_marking, final_marking)
        end_time = time.time()

        runtime[log_path, discovery_algorithm] = end_time - start_time

    return models[log_path, discovery_algorithm]


def read_log(log_path):
    if log_path in logs:
        return logs[log_path]
    else:
        try:
            log = pm4py.read_xes(log_path)
            logs[log_path] = log
            return log
        except Exception:
            print("The log does not exist !")


def load_all_logs_into_cache():
    global log_paths, no_logs, log, algorithm_portfolio, cached_variables, y
    log_paths = gather_all_xes("./")[:no_logs]
    y = [None] * len(log_paths)
    for i in range(no_logs):
        read_log(log_paths[i])
        for discovery_algorithm in algorithm_portfolio:
            read_model(log_paths[i], discovery_algorithm)

    cached_variables["models"] = models
    cached_variables["logs"] = logs
    cached_variables["log_paths"] = log_paths

    with open("cache.pkl", "wb") as file:
        pickle.dump(cached_variables, file)


def load_all_logs_from_cache():
    global cached_variables, log_paths, logs, models
    log_paths = gather_all_xes("./")[:no_logs]
    if os.path.getsize("cache.pkl") == 0:
        load_all_logs_into_cache()
    else:
        with open("cache.pkl", "rb") as file:
            cached_variables = pickle.load(file)
        log_paths = cached_variables["log_paths"]
        logs = cached_variables["logs"]
        models = cached_variables["models"]
