import subprocess
import pm4py
import os
home_dir = "/Users/tarekjunied/Documents/Universität/BachelorThesis"


def remove_extension(filename):
    base = os.path.basename(filename)  # Get the filename without path
    name_without_extension = os.path.splitext(base)[0]  # Remove the extension
    return name_without_extension

def discover_petri_net_fodina(log_path,timeout_minutes=2):

    log_name = remove_extension(log_path)
    command_cd = "cd discovery/structuredminer"
    command = f"java -jar StructuredMiner.jar fo {str(timeout_minutes)} {log_path} {home_dir}/src/discovery/models/{log_name}"
    command_cd_back = "cd ..;cd .."
    print(command)
    result = subprocess.run(
        f"{command_cd};{command};{command_cd_back}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    print("Output:")
    output = result.stdout
    error = result.stderr
    print(output)

    dest = f"{home_dir}/src/discovery/models/{log_name}.bpmn"
    print(f"Success: model stored to {dest}")

    bpmn = pm4py.read.read_bpmn(dest)
    net, im, fm = pm4py.convert_to_petri_net(bpmn)

    return (net, im, fm)


