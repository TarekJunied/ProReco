import globals
import time
import os
import pm4py
from measures import compute_measure, read_measure_entry
from filehelper import select_smallest_k_logs
from utils import read_models, read_model

if __name__ == "__main__":
    log_paths = select_smallest_k_logs(50, "../logs/training")
    output_dict = {}
    read_models(log_paths)
    for measure_name in globals.measures:
        avg_time = 0
        start_time = time.time()
        skipped = 0
        for log_path in log_paths:
            for discovery_algorithm in globals.algorithm_portfolio:
                try:
                    compute_measure(
                        log_path, discovery_algorithm, measure_name)
                except Exception as e:
                    print(e)

        end_time = time.time()
        avg_time = end_time - start_time

        output_dict[measure_name] = avg_time

    os.system('clear')
    sorted_items = sorted(output_dict.items(), key=lambda x: x[1])
    # Print each key and its corresponding value
    for key, value in sorted_items:
        print(f"{key}: {value}")
