import subprocess
import datetime
import os
import shutil
import random
# TODO remove relative paths and perhaps add more flexiblity by visting java project again


def clear_folder(folder_path):
    try:
        # Check if the folder exists
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Iterate through all items in the folder
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)  # Remove files
                elif os.path.isdir(item_path):
                    # Remove subdirectories and their contents
                    shutil.rmtree(item_path)
            print(f"Folder {folder_path} has been emptied.")
        else:
            print(f"Folder {folder_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_random_process(and_branches=5,
                          xor_branches=5,
                          loop_weight=0.1,
                          single_activity_weight=0.2,
                          skip_weight=0.1,
                          sequence_weight=0.7,
                          and_weight=0.3,
                          xor_weight=0.3,
                          max_depth=3,
                          data_object_probability=0.1):
    storage_path = "./processes/process_" + \
        str(datetime.datetime.now().time()) + ".plg"

    command_list = ["java", "-jar", "ProcessGenerator.jar",
                    "-ab", str(and_branches), "-xb", str(xor_branches),
                    "-l", str(loop_weight), "-sa", str(single_activity_weight),
                    "-sw", str(skip_weight), "-sq", str(sequence_weight),
                    "-aw", str(and_weight), "-xw", str(xor_weight),
                    "-md", str(max_depth), "-dop", str(data_object_probability),
                    "-fd", storage_path]

    command = " ".join(map(str, command_list))
    print(command)

    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    print("Output:")
    output = result.stdout
    error = result.stderr
    print(output)

    if len(error) == 0:
        print(f"Success: process stored to {storage_path}")
    else:
        print("An error has occured.")
        print("Errors:")
        print(error)

    return storage_path


def create_log_from_model(model_path, no_traces=1000):
    storage_path = "./logs/log_" + str(datetime.datetime.now().time()) + ".xes"

    command_list = [
        "java", "-jar", "LogGenerator.jar",
        "-l", storage_path,
        "-m", model_path,
        "-c", str(no_traces)
    ]
    command = " ".join(map(str, command_list))
    print(command)
    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    print("Output:")
    output = result.stdout
    error = result.stderr
    print(output)

    if len(error) == 0:
        print(f"Success: log stored to {storage_path}")
    else:
        print("An error has occured.")
        print("Errors:")
        print(error)


clear_folder("./processes")
clear_folder("./logs")

for i in range(0, 100):
    random_and_branches = random.randint(0, 7)
    random_xor_branches = random.randint(0, 5)
    random_loop_weight = random.uniform(0, 0.5)
    random_single_activity_weight = random.uniform(0,  0.3)
    random_sequence_weight = random.uniform(0.2, 1)
    random_and_weight = random.uniform(0, 0.5)
    random_xor_weight = random.uniform(0, 0.5)
    random_max_depth = random.randint(1, 7)
    random_data_object_probability = random.uniform(0, 0.4)

    cur_proc = create_random_process(and_branches=random_and_branches,
                                     xor_branches=random_xor_branches,
                                     loop_weight=random_loop_weight,
                                     single_activity_weight=random_single_activity_weight,
                                     sequence_weight=random_sequence_weight,
                                     and_weight=random_and_weight,
                                     xor_weight=random_xor_weight,
                                     max_depth=random_max_depth,
                                     data_object_probability=random_data_object_probability)
    create_log_from_model(cur_proc, random.randint(1000, 2000))
