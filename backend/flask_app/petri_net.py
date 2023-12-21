import pm4py
import os
from filehelper import gather_all_xes, get_all_ready_logs
from utils import read_model


def create_json_petri_net(petri_net):
    (net, im, fm) = petri_net
    places = net.places
    transitions = net.transitions
    arcs = net.arcs

    for place in places:
        print(place)

    for transition in transitions:
        input(transition)

    for arc in arcs:
        input(arc.source_name, arc.source.label)


if __name__ == "__main__":

    log_paths = gather_all_xes("../logs/modified_eventlogs")

    log_path_to_predict = log_paths[0]

    petri_net = read_model(log_path_to_predict, "alpha")

    (net, im, fm) = petri_net
    pm4py.write_pnml(net, initial_marking, final_marking, "petri.pnml")
    pm4py.vis.save_vis_petri_net(net, im, fm, "./testing_petri.png")
    pm4py.vis
    create_json_petri_net(petri_net)
