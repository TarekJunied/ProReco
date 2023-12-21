import pm4py
import matplotlib.pyplot as plt
import os
import json
import networkx as nx
from filehelper import gather_all_xes, get_all_ready_logs
from utils import read_model


def create_json_petri_net(petri_net):
    (net, im, fm) = petri_net

    G = nx.DiGraph()

    # Add places and transitions as nodes
    for place in net.places:
        G.add_node(place.name, type='place')
    for transition in net.transitions:
        G.add_node(transition.name, type='transition')

    # Add arcs as edges
    for arc in net.arcs:
        G.add_edge(arc.source.name, arc.target.name)

    # Apply a layout algorithm
    pos = nx.spring_layout(G)

    petri_net_dict = {
        "places": [{"x": pos[place.name][0], "y": pos[place.name][1], "id": place.name} for place in net.places],
        "transitions": [{"x": pos[transition.name][0], "y": pos[transition.name][1], "id": transition.name, "label": transition.label} for transition in net.transitions],
        "links": [{"sourceid": arc.source.name, "targetid": arc.target.name} for arc in net.arcs]
    }
    return json.dumps(petri_net_dict)

    """
    plt.figure(figsize=(12, 8))  # Adjust the size of the figure as needed
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            edge_color='gray', node_size=2000, font_size=10)

    # Draw edge labels (optional)
    # Replace 'weight' with the appropriate attribute if necessary
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Save the graph as a PNG file
    plt.savefig("./petri_net.png")

    # Optionally, show the graph in an interactive window (remove this line if running in a non-interactive environment)
    plt.show()

    """


if __name__ == "__main__":

    log_paths = gather_all_xes("../logs/training")

    log_path_to_predict = log_paths[0]

    petri_net = read_model(log_path_to_predict, "heuristic")

    input(type(petri_net))
    (net, im, fm) = petri_net
    pm4py.write_pnml(net, im, fm, "BETRIBETRIB.pnml")
    pm4py.vis.save_vis_petri_net(net, im, fm, "./testing_petri.png")
    create_json_petri_net(petri_net)
