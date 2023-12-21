import pm4py
import matplotlib.pyplot as plt
import pygraphviz as pgv
import os
import json
import networkx as nx
from PIL import Image
from filehelper import gather_all_xes, get_all_ready_logs
from utils import read_model
import os
import sys
from pm4py.visualization.petri_net import visualizer as pn_visualizer


def custom_layout(petri_net):
    (net, im, fm) = petri_net
    file_path = "./fuckyou.png"
    format = os.path.splitext(file_path)[1][1:].lower()
    from pm4py.visualization.petri_net import visualizer as pn_visualizer
    gviz = pn_visualizer.apply(net, im, fm,
                               parameters={pn_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: format, "bgcolor": "white", "decorations": None, "debug": False, "set_rankdir": "LR"})

    output = gviz.pipe(format='plain').decode('utf-8')

    # Parse the output to get positions
    positions = {}
    for line in output.splitlines():
        parts = line.split()
        if parts[0] == 'node':
            node_id = parts[1]
            x, y = float(parts[2]), float(parts[3])
            positions[node_id] = (x, y)

    # 'positions' dictionary contains the node positions
    print(positions)


def extract_xy_from_graphviz_pos(string):
    try:
        x_str, y_str = string.split(',')
        x = float(x_str)
        y = float(y_str)
        return x, y
    except ValueError:
        raise ValueError(
            "Invalid format. The string should be in 'x,y' format.")


def get_node_type(pgv_node):
    if pgv_node["shape"] == "circle":
        return "place"
    elif pgv_node["shape"] == "box":
        return "transition"
    else:
        print("invalid node kind")
        return


def create_json_petri_net(petri_net):
    (net, im, fm) = petri_net

    pm4py.vis.save_vis_petri_net(net, im, fm, "./temp_petri_net.png")

    with Image.open("./temp_petri_net.png") as img:
        total_width, total_height = img.size

    gviz = pn_visualizer.apply(net, im, fm)

    dot_string = gviz.source

    A = pgv.AGraph(string=dot_string)
    A.layout(prog='dot')

    place_dict_list = [{"x": extract_xy_from_graphviz_pos(node.attr['pos'])[0] / total_width,
                        "y": extract_xy_from_graphviz_pos(node.attr['pos'])[1] / total_height,
                        "id": str(node),
                        "label": node.attr["label"]}
                       for node in A.nodes() if node.attr["shape"] == "circle"]

    transition_dict_list = [{"x": extract_xy_from_graphviz_pos(node.attr['pos'])[0] / total_width,
                             "y": extract_xy_from_graphviz_pos(node.attr['pos'])[1] / total_height,
                             "id": str(node),
                             "label": node.attr["label"]}
                            for node in A.nodes() if node.attr["shape"] == "box"]

    link_dict_list = [{"sourceid": edge[0], "targetid": edge[1]}
                      for edge in A.edges()]

    for edge in A.edges():
        input(edge)
        input(edge[0])
        input(edge[1])

    petri_net_dict = {
        "places": place_dict_list,
        "transitions": transition_dict_list,
        "links": link_dict_list
    }
    print("done")

    return petri_net_dict


if __name__ == "__main__":

    log_paths = gather_all_xes("../logs/training")

    log_path_to_predict = log_paths[0]

    petri_net = read_model(log_path_to_predict, "heuristic")

    create_json_petri_net(petri_net)
