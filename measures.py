from utils import read_model, read_log
import pm4py
import sys
import globals

# Fitness measures


def measure_token_fitness(log_path, discovery_algorithm):
    log = read_log(log_path)
    petri_net, initial_marking, final_marking = read_model(
        log_path, discovery_algorithm)
    result = pm4py.conformance.fitness_token_based_replay(
        log, petri_net, initial_marking, final_marking)
    print(discovery_algorithm, result["average_trace_fitness"])
    return result["average_trace_fitness"]


def measure_alignment_fitness(log_path, discovery_algorithm):
    log = read_log(log_path)
    petri_net, initial_marking, final_marking = read_model(
        log_path, discovery_algorithm)
    result = pm4py.conformance.fitness_alignments(
        log, petri_net, initial_marking, final_marking)
    print(discovery_algorithm, result["average_trace_fitness"])
    return result["average_trace_fitness"]

# PRECISION


def measure_token_precision(log_path, discovery_algorithm):
    log = read_log(log_path)
    petri_net, initial_marking, final_marking = read_model(
        log_path, discovery_algorithm)
    result = pm4py.conformance.precision_token_based_replay(
        log, petri_net, initial_marking, final_marking)
    print(discovery_algorithm, result)
    return result


def measure_alignment_precision(log_path, discovery_algorithm):
    log = read_log(log_path)
    petri_net, initial_marking, final_marking = read_model(
        log_path, discovery_algorithm)
    result = pm4py.conformance.precision_alignments(
        log, petri_net, initial_marking, final_marking)
    print(discovery_algorithm, result)
    return result


def number_of_places(net):
    return len(net._PetriNet__places)


def number_of_transitions(net):
    return len(net._PetriNet__transitions)


def number_of_arcs(net):
    return len(net._PetriNet__arcs)

# SIMPLICITY MEAURES


def measure_no_total_elements(log_path, discovery_algorithm):
    """Takes in net only as input
    Args:
        net: net, as returned by a discovery algorithm
    """
    net, _, _ = read_model(log_path, discovery_algorithm)
    return number_of_arcs(net) + number_of_places(net) + number_of_transitions(net)


def measure_node_arc_degree(log_path, discovery_algorithm):
    net, _, _ = read_model(log_path, discovery_algorithm)
    return number_of_arcs(net) / (number_of_transitions(net) + number_of_places(net))


# performance measures
def measure_runtime(log_path, discovery_algorithm):
    model = read_model(log_path, discovery_algorithm)
    return globals.runtime[log_path, discovery_algorithm]


def measure_used_memory(log_path, discovery_algorithm):
    model = read_model(log_path, discovery_algorithm)
    return sys.getsizeof(model)


def compute_measure(log_path, discovery_algorithm, measure_name):
    if measure_name == "token_fitness":
        return measure_token_fitness(log_path, discovery_algorithm)
    elif measure_name == "alignment_fitness":
        return measure_alignment_fitness(log_path, discovery_algorithm)
    elif measure_name == "token_precision":
        return measure_token_precision(log_path, discovery_algorithm)
    elif measure_name == "alignment_precision":
        return measure_alignment_precision(log_path, discovery_algorithm)
    elif measure_name == "no_total_elements":
        return measure_no_total_elements(log_path, discovery_algorithm)
    elif measure_name == "node_arc_degree":
        return measure_node_arc_degree(log_path, discovery_algorithm)
    elif measure_name == "runtime":
        return measure_runtime(log_path, discovery_algorithm)
    elif measure_name == "used_memory":
        return measure_used_memory(log_path, discovery_algorithm)
    else:
        raise ValueError("Invalid measure name")

def init_max_target_vector(log_path,log_index,measure_name):
    cur_max = float("-inf")
    for discovery_algorithm in globals.algorithm_portfolio:
        algo_val = compute_measure(log_path, discovery_algorithm, measure_name)
        if algo_val > cur_max:
            cur_max = algo_val
            globals.y[log_index] = discovery_algorithm
    globals.target_vectors[log_path, measure_name] = globals.y[log_index]

def init_min_target_vector(log_path,log_index,measure_name):
    cur_min = float("-inf")
    for discovery_algorithm in globals.algorithm_portfolio:
        algo_val = compute_measure(log_path, discovery_algorithm, measure_name)
        if algo_val < cur_min:
            cur_min = algo_val
            globals.y[log_index] = discovery_algorithm
    globals.target_vectors[log_path,measure_name] = globals.y[log_index]

def init_target_entry(log_path, log_index,measure_name):
    if globals.measures[measure_name] == "max":
        init_max_target_vector(log_path,log_index,measure_name)
    if globals.measures[measure_name] == "min":
        init_min_target_vector(log_path,log_index,measure_name)
    globals.target_vectors[log_path, measure_name] = globals.y[log_index]

def init_target_vector(measure_name):
    globals.y = [None] * len(globals.training_logs_paths)
    n = len(globals.training_logs_paths)
    for i in range(n):
        init_target_entry(globals.training_logs_paths[i],i,measure_name)
    globals.pickled_variables["target_vectors"] = globals.target_vectors
