import subprocess
import pm4py
import os
home_dir = "~/Documents/Universität/BachelorThesis"


def remove_extension(filename):
    base = os.path.basename(filename)  # Get the filename without path
    name_without_extension = os.path.splitext(base)[0]  # Remove the extension
    return name_without_extension


def discover_petri_net_split(log_path, parallelism_threshold=0.1, frequency_threshold=0.4, remove_or_joins=False):

    log_name = remove_extension(log_path)

    model_path = f"./discovery/models/split_{log_name}"

    command = f"java -cp discovery/splitminer/splitminer.jar:./discovery/splitminer/lib/* au.edu.unimelb.services.ServiceProvider SMPN {parallelism_threshold} {frequency_threshold}\
    {remove_or_joins} {log_path} {model_path}"

    input(command)

    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    print("Output:")
    output = result.stdout
    error = result.stderr
    print(output)
    if len(error) != 0:
        print("Error:")
        print(error)

    dest = f"{model_path}.pnml"

    print(f"Success: model stored to {dest}")

    input("hi")
    net, im, fm = pm4py.read.read_pnml(dest)

    return net, im, fm
