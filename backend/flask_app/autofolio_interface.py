import csv
import globals
from features import read_single_feature
from utils import get_log_name
from filehelper import gather_all_xes, get_all_ready_logs_multiple
from measures import read_measure_entry
import numpy as np


def create_csv_from_list(data,filepath):
    """
    data = [
    ['Name', 'Age', 'City'],
    ['John Doe', 25, 'New York'],
    ['Jane Smith', 30, 'San Francisco'],
    ['Bob Johnson', 22, 'Los Angeles']
    ]
    Args:
        look at above
    """
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
    
        # Write the header
        writer.writerow(data[0])
    
        # Write the remaining rows
        writer.writerows(data[1:])

        print(f'CSV file "{filepath}" has been created.')


def create_feature_csv(log_paths,filepath):
    first_row = [""] + globals.selected_features
    data = [first_row]
    i = 1
    for log_path in log_paths:
        cur_row =[f"inst{i}"]
        for feature in globals.selected_features:
            cur_row +=[read_single_feature(log_path,feature)]
        data += [cur_row]
        i+=1

    create_csv_from_list(data,filepath)


def create_performance_csv(log_paths,measure_name,filepath):
    first_row = [""] + globals.algorithm_portfolio
    data = [first_row]
    i = 1
    for log_path in log_paths:
        cur_row =[f"inst{i}"]
        for discovery_algorithm in globals.algorithm_portfolio:
            cur_row +=[read_measure_entry(log_path,discovery_algorithm,measure_name)]
        data += [cur_row]
        i+=1

    create_csv_from_list(data,filepath)
    






