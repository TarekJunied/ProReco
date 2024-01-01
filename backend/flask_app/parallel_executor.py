import os
import time
import subprocess
from filehelper import gather_all_xes
from utils import read_model, read_log, load_cache_variable, store_cache_variable, generate_log_id, generate_cache_file,  read_log
import logging
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from tqdm.contrib.concurrent import process_map  # Use process_map from tqdm
from feature_controller import read_feature_matrix, read_feature_vector, get_total_feature_functions_dict, read_single_feature
from feature_selection import regression_read_optimal_features
from measures import read_target_entries, read_target_entry, read_classification_target_vector, read_measure_entry
from filehelper import gather_all_xes, split_file_path, get_all_ready_logs
from LogGenerator.log_generator import create_random_log
import multiprocessing
import globals
import random
import sys
import pm4py
import os


def get_number_of_not_ready_logs(log_paths_dir):
    total_logs = gather_all_xes(log_paths_dir)
    ready_logs = get_all_ready_logs(
        log_paths, globals.selected_features, globals.algorithm_portfolio)
    return len(total_logs) - len(ready_logs)


def write_list_to_file(lst, file_name):
    """
    Writes each element of the list to a file, each on a new line.
    Args:
    lst: The list of elements to write.
    file_name: The name of the file to write to.
    """
    with open(file_name, 'w') as file:
        for element in lst:
            file.write(str(element) + '\n')


def generate_job_script(job_name, jobscript_path, number_of_tasks, cpus_per_task, outputs_path, execution_command,  execution_time_string="72:00:00"):
    script = "#!/usr/local_rwth/bin/zsh\n"
    script += f"#SBATCH --job-name={job_name}\n"
    script += f"#SBATCH --mem=10G\n"
    script += f"#SBATCH --output={outputs_path}/{job_name}_OUTPUT.txt\n"
    script += f"#SBATCH --error={outputs_path}/{job_name}_ERROR.txt\n"
    script += f"#SBATCH --account=thes1569\n"
    script += f"#SBATCH --time={execution_time_string}\n"
    script += f"echo \"Now starting {job_name}\" \n"
    script += f"{execution_command}\n"

    with open(jobscript_path, 'w') as file:
        file.write(script)

    return jobscript_path


def generate_job_array_script(job_name, jobscript_path, array_length, outputs_path, execution_command,  execution_time_string="72:00:00"):
    script = "#!/usr/local_rwth/bin/zsh\n"
    script += f"#SBATCH --job-name={job_name}\n"
    script += f"#SBATCH --array=1-{array_length}%800\n"
    script += f"#SBATCH --mem=10G\n"
    script += f"#SBATCH --output={outputs_path}/{job_name}.out\n"
    script += f"#SBATCH --error={outputs_path}/{job_name}.err\n"
    script += f"#SBATCH --account=thes1569\n"
    script += f"#SBATCH --time={execution_time_string}\n"
    script += f"echo \"Now starting {job_name}\" \n"
    script += f"echo Job $SLURM_ARRAY_TASK_ID of $job_name starting at: $(date)\n"
    script += f"start=$(date +%s)\n"
    script += f"{execution_command}\n"
    script += f"end=$(date +%s)\n"
    script += f"echo Job $SLURM_ARRAY_TASK_ID of $job_name finished at: $(date)\n"
    script += f"echo Duration: $((end-start)) seconds.\n"
    script += f"if [ $SLURM_ARRAY_TASK_ID -eq {array_length} ]; then\n"
    script += f"echo All jobs done.\n"
    script += f"fi\n"

    with open(jobscript_path, 'w') as file:
        file.write(script)
    return jobscript_path


def feature_init(log_path):
    feature_portfolio = globals.selected_features
    for feature in feature_portfolio:
        print(feature)
        read_single_feature(log_path, feature)


def start_parallel_execution_job(mode, log_paths_list, job_name):
    dir_name = f"/home/qc261227/Recommender/RecommenderSystem/backend/flask_app/parallel/{job_name}"
    array_length = len(log_paths_list)

    middle_arg = "\"${SLURM_ARRAY_TASK_ID}p\""
    execution_command = f"LOG_PATH=$(sed -n {middle_arg} {dir_name}/log_paths.txt)\n"
    if mode == "feature":
        execution_command += f"/usr/bin/python3.9 feature_initor.py $LOG_PATH\n"
    if mode == "algo":
        execution_command += f"/usr/bin/python3.9 algo_initor.py $LOG_PATH\n"
    if mode == "all":
        execution_command += f"/usr/bin/python3.9 all_initor.py $LOG_PATH\n"
    if mode == "measure":
        execution_command += f"/usr/bin/python3.9 measure_initor.py $LOG_PATH\n"

    if not os.path.exists(dir_name):
        # Create the directory
        os.makedirs(dir_name)

    write_list_to_file(log_paths_list, f"{dir_name}/log_paths.txt")

    # Check if the directory already exists

    script_path = generate_job_array_script(
        job_name, f"{dir_name}/{job_name}_jobscript.sh", array_length, dir_name, execution_command)

    return script_path


def run_sbatch_script(script_path):
    try:
        result = subprocess.run(
            ['sbatch', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Capture and print standard output and error
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        # If the submission was successful, result.stdout will contain the job info
        if result.returncode == 0:
            print("Submitted successfully!")
        else:
            print("Failed to submit job")
    except Exception as e:
        print(f"Error occurred: {e}")
        input("next")


def get_undone_logs(all_logs, mode):
    negative_list = []
    if mode == "feature":
        negative_list = get_all_ready_logs(
            all_logs, globals.selected_features, [], [])
    if mode == "algo":
        negative_list = get_all_ready_logs(
            all_logs, [], globals.algorithm_portfolio, [])
    if mode == "measure":
        negative_list = get_all_ready_logs(
            all_logs, [], globals.algorithm_portfolio, globals.measures_list)

    if mode == "all":
        negative_list = get_all_ready_logs(
            all_logs, globals.selected_features, globals.algorithm_portfolio, globals.measures_list)
    print(f"we have {len(negative_list)} done logs")
    return [x for x in all_logs if x not in negative_list]


def submit_optimal_featues_compuation_regressor(regression_method, discovery_algorithm, measure_name):
    job_name = f"{regression_method}_{discovery_algorithm}_{measure_name}_features"
    dir_name = f"/home/qc261227/Recommender/RecommenderSystem/backend/flask_app/parallel/{job_name}"
    if not os.path.exists(dir_name):
        # Create the directory
        os.makedirs(dir_name)

    execution_command = f"/usr/bin/python3.9 feature_selection.py {regression_method} {discovery_algorithm} {measure_name}"
    jobscript = generate_job_script(
        job_name, f"{dir_name}/{job_name}.sh", "1", "1", dir_name, execution_command, "12:00:00")
    run_sbatch_script(jobscript)


def read_optimal_features_for_regressors_in_parallel():
    for regression_method in globals.regression_methods:
        for discovery_algorithm in globals.algorithm_portfolio:
            for measure_name in globals.measures_list:
                submit_optimal_featues_compuation_regressor(
                    regression_method, discovery_algorithm, measure_name)

    input("done submitting all feature jobs")


if __name__ == "__main__":
    globals.selected_features = list(get_total_feature_functions_dict().keys())
    globals.algorithm_portfolio = ["alpha", "heuristic",
                                   "inductive", "ILP", "split", "alpha_plus", "inductive_infrequent", "inductive_direct"]

    read_optimal_features_for_regressors_in_parallel()
    modes = ["feature", "algo", "measure"]
    modes = ["all"]
    log_paths_dirs = [f"/rwthfs/rz/cluster/home/qc261227/Recommender/RecommenderSystem/backend/logs/{log_path}" for log_path in [
        "modified_eventlogs", "training", "testing"]]

    all_logs = gather_all_xes("../logs/training") + gather_all_xes(
        "../logs/testing") + gather_all_xes("../logs/modified_eventlogs")
    ready_logs = get_all_ready_logs(
        all_logs, globals.selected_features, globals.algorithm_portfolio, globals.measures_list)

    """"
    done = [(modes[0], log_paths_dirs[0])]

    name = "all_logs"
    mode = "all"
    log_paths_list = get_undone_logs(all_logs, mode)[:950]
    input(len(log_paths_list))
    input(f"{mode}_{name}")
    script_path = start_parallel_execution_job(
        mode, log_paths_list, f"{mode}_{name}")
    run_sbatch_script(script_path)
    input("next ? ")

    for log_paths_dir in log_paths_dirs:
        for mode in modes:
            if (mode, log_paths_dir) not in done:
                name = split_file_path(log_paths_dir)["filename"]
                all_logs = gather_all_xes(log_paths_dir)

                log_paths_list = get_undone_logs(all_logs, mode)[:1000]
                input(len(log_paths_list))
                input(f"{mode}_{name}")
                script_path = start_parallel_execution_job(
                    mode, log_paths_list, f"{mode}_{name}")
                run_sbatch_script(script_path)
                input("next ? ")
    """
