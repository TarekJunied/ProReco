import globals
import time
import os
from measures import compute_measure, read_measure_entry
from filehelper import select_smallest_k_logs
from utils import read_models

if __name__ == "__main__":
    log_paths = select_smallest_k_logs(50, "../logs/training")
    """"
    output_str = "HIII \n"


    read_models(log_paths)

    for measure_name in globals.measures:
        avg_time = 0
        start_time = time.time()
        skipped = 0
        for log_path in log_paths:
            for discovery_algorithm in globals.algorithm_portfolio:
                compute_measure(
                    log_path, discovery_algorithm, measure_name)

        end_time = time.time()
        avg_time = end_time - start_time

        output_str += f"measure name: {measure_name}\n"
        output_str += f"avg_time: {avg_time}\n"


    input(f"skipped {skipped}")
    os.system('clear')
    print(output_str)
    """
