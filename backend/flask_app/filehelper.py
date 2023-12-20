import os
import globals
import pickle
import zipfile
import pytz
import re
import numpy as np
from datetime import datetime
import tarfile


def load_cache_variable(cache_file_path):
    with open(cache_file_path, 'rb') as cache_file:
        loaded_variable = pickle.load(cache_file)
    print(f"Variable loaded from cache file: {cache_file_path}")
    return loaded_variable


def split_file_path(file_path):
    # Split the file path into directory, filename, and extension
    directory, file_name_with_extension = os.path.split(file_path)
    file_name, file_extension = os.path.splitext(file_name_with_extension)

    return {
        'directory': directory,
        'filename': file_name,
        'extension': file_extension
    }


def generate_log_id(log_path):
    return get_file_name(log_path)


def all_files_exist(file_list):

    for file_path in file_list:
        if not os.path.exists(file_path):
            print("File missing:")
            print(file_path)
            return False
    return True


def gather_all_ext(dir_path, extension):
    xes_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(extension):
                xes_files.append(os.path.join(root, file))

    return xes_files


def contains_space(filepath):

    # Check if the file path contains a space
    if ' ' in filepath:
        return True
    else:
        return False


def replace_substring_and_rename_file(file_path, old_substring, new_substring):
    # Get the directory and file name from the file path
    directory, file_name = os.path.split(file_path)

    # Replace the old substring with the new substring in the file name
    new_file_name = file_name.replace(old_substring, new_substring)

    # Create the new file path by joining the directory and new file name
    new_file_path = os.path.join(directory, new_file_name)

    # Rename the file if the new name is different
    if new_file_path != file_path:
        try:
            os.rename(file_path, new_file_path)
        except OSError as e:
            return f"Error renaming {file_path}: {e}"

    print(f"changed {file_path} to {new_file_path}")

    return new_file_path


def find_files_with_substring(directory, substring):
    matching_files = []

    # Walk through the directory and its subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            # Check if the substring is present in the file name
            if substring in file:
                # Get the full path of the matching file
                file_path = os.path.join(root, file)
                matching_files.append(file_path)

    return matching_files


def get_file_name(file_path):
    # Use os.path.basename to get the file name with extension
    file_name_with_extension = os.path.basename(file_path)

    # Use os.path.splitext to split the file name and extension
    file_name, file_extension = os.path.splitext(file_name_with_extension)

    return file_name


def gather_all_csv(dir_path):
    return gather_all_ext(dir_path, ".csv")


def gather_all_xes(dir_path):
    return gather_all_ext(dir_path, ".xes")


def select_smallest_k_logs(k, dir_path):
    # Create a list of tuples containing (file_path, file_size)
    globals.training_logs_paths = gather_all_xes(dir_path)
    files_with_sizes = [(file_path, os.path.getsize(file_path))
                        for file_path in globals.training_logs_paths]

    # Sort the list of tuples by file size
    sorted_files = sorted(files_with_sizes, key=lambda x: x[1])

    # Extract the sorted file paths from the sorted list of tuples
    sorted_file_paths = [file_path for file_path, _ in sorted_files]

    return sorted_file_paths[:k]


def remove_extension(filename):
    base = os.path.basename(filename)  # Get the filename without path
    name_without_extension = os.path.splitext(base)[0]  # Remove the extension
    return name_without_extension


def get_all_ready_logs_multiple(log_paths):
    current = set(log_paths)

    for measure in globals.measures_list:
        ready_logs = set(get_all_ready_logs(current, measure))
        current = current.intersection(ready_logs)

    return list(current)


def get_all_logs_with_ready_features(log_paths, feature_list):
    ready_logs = []
    for log_path in log_paths:
        file_list = []
        log_id = generate_log_id(log_path)
        log_cache = f"{globals.flask_app_path}/cache/logs/{log_id}.pkl"
        file_list += [log_cache]
        for feature in feature_list:
            feature_path = f"{globals.flask_app_path}/cache/features/{feature}_{log_id}.pkl"
            file_list += [feature_path]

        no_problem = True
        for file in file_list:
            try:
                x = load_cache_variable(file)
            except Exception:
                no_problem = False
                print(f"{file} is missing")

        if no_problem:
            ready_logs += [log_path]

    return ready_logs


def get_all_ready_logs(log_paths, measure_name):
    ready_logs = []
    for log_path in log_paths:
        file_list = []
        log_id = generate_log_id(log_path)
        log_cache = f"{globals.flask_app_path}/cache/logs/{log_id}.pkl"
        file_list += [log_cache]
        for discovery_algorithm in globals.algorithm_portfolio:
            model_path = f"{globals.flask_app_path}/cache/models/{discovery_algorithm}_{log_id}.pkl"
            measure_cache = f"{globals.flask_app_path}/cache/measures/{discovery_algorithm}_{measure_name}_{log_id}.pkl"
            file_list += [model_path, measure_cache]
        for feature in globals.selected_features:
            feature_path = f"{globals.flask_app_path}/cache/features/{feature}_{log_id}.pkl"
            file_list += [feature_path]

        no_problem = True
        for file in file_list:
            if not os.path.exists(file):
                no_problem = False
                print(f"{file} is missing")

        if no_problem:
            ready_logs += [log_path]

    return ready_logs


def unzip_all(zip_path, extract_path):
    # Check if the provided path is a directory
    if not os.path.isdir(extract_path):
        os.makedirs(extract_path)

    # Iterate over all files in the given directory
    for file_name in os.listdir(zip_path):
        file_path = os.path.join(zip_path, file_name)

        # Check if the file is a zip or tar file
        if zipfile.is_zipfile(file_path):
            # Unzip the file
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            print(f"Unzipped: {file_path}")

            # Recursively call the function for the extracted contents
            unzip_all(os.path.join(extract_path,
                      file_name.split('.')[0]), extract_path)

        elif tarfile.is_tarfile(file_path):
            # Untar the file
            with tarfile.open(file_path, 'r:gz') as tar_ref:
                tar_ref.extractall(extract_path)
            print(f"Untarred: {file_path}")

            # Recursively call the function for the extracted contents
            unzip_all(os.path.join(extract_path,
                      file_name.split('.')[0]), extract_path)


def add_timestamps_to_log_path(file_path):
    """
    Adds unique date lines to each <event> tag in the XML file at file_path.

    :param file_path: Path to the input XML file.
    :param dates: A list of tuples, where each tuple contains two date strings (start and end).
    :param output_file_path: Path to the output XML file. If None, the input file is overwritten.
    """
    # Read the contents of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    updated_content = []
    inside_event = False
    for line in content:
        updated_content.append(line)
        if '<event>' in line:
            inside_event = True
        elif '</event>' in line:
            inside_event = False
        elif inside_event and '<string' in line:
            try:
                utc_now = datetime.now(pytz.utc)
                timestamp = utc_now.strftime('%Y-%m-%dT%H:%M:%S+00:00')
                date_lines = f'\t\t\t<date key="time:start_timestamp" value="{timestamp}" />\n'
                date_lines += f'\t\t\t<date key="time:timestamp" value="{timestamp}" />\n'
                updated_content.append(date_lines)
            except StopIteration:
                print("Error in processing dates.")
                break

    filename = split_file_path(file_path)["filename"]
    directory = split_file_path(file_path)["directory"]
    # Write the updated content back to the file or to a new file
    output_file_path = f"/home/qc261227/Recommender/RecommenderSystem/backend/logs/modified_eventlogs/modified_{filename}.xes"
    # output_file_path = file_path
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.writelines(updated_content)


if __name__ == "__main__":
    log_paths = gather_all_xes("../logs/process_meta_learning_logs")
    for log_path in log_paths:
        print(log_path)
        add_timestamps_to_log_path(log_path)
