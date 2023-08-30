import subprocess
import pm4py
import os
home_dir = "/Users/tarekjunied/Documents/Universität/BachelorThesis"


def remove_extension(filename):
    base = os.path.basename(filename)  # Get the filename without path
    name_without_extension = os.path.splitext(base)[0]  # Remove the extension
    return name_without_extension


def discover_petri_net_split(log_path, parallelism_threshold=0.1, frequency_threshold=0.4, remove_or_joins=False):

    log_name = remove_extension(log_path)
    command_cd = "cd discovery/splitminer"
    command = f"java -cp splitminer.jar:./lib/* au.edu.unimelb.services.ServiceProvider SMPN {parallelism_threshold} {frequency_threshold}\
    {remove_or_joins} {log_path} ../models/{log_name}"
    command_cd_back = "cd ..;cd .."
    print(command)

    result = subprocess.run(
        f"{command_cd};{command};{command_cd_back}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    print("Output:")
    output = result.stdout
    error = result.stderr
    print(output)
    print("Error:")
    print(error)

    dest = f"{home_dir}/src/discovery/models/{log_name}.pnml"

    print(f"Success: model stored to {dest}")

    net, im, fm = pm4py.read.read_pnml(
        f"{home_dir}/src/discovery/models/{log_name}.pnml")
    return net, im, fm
