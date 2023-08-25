from utils import read_model,read_log
import pm4py



def fitness_token_based_replay(log_path,discovery_algorithm):
    log = read_log(log_path)
    petri_net,initial_marking,final_marking = read_model(log_path,discovery_algorithm)
    result = pm4py.conformance.fitness_token_based_replay(log, petri_net,initial_marking, final_marking)
    print(discovery_algorithm, result["average_trace_fitness"])
    return result["average_trace_fitness"]

def precision_token_based_replay(log_path,discovery_algorithm):
    log = read_log(log_path)
    petri_net,initial_marking,final_marking = read_model(log_path,discovery_algorithm)
    result = pm4py.conformance.precision_token_based_replay(log, petri_net,initial_marking, final_marking)
    print(discovery_algorithm, result)
    return result

def model_simplicity(log_path, discovery_algorithm):
    log = read_log(log_path)
    petri_net,initial_marking,final_marking = read_model(log_path,discovery_algorithm)
