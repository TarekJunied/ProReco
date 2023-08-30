import subprocess
import pm4py


def discover_petri_net_split(log_path, model_destination, parallelism_threshold=0.1, frequency_threshold=0.4, remove_or_joins=False):

    command = f"java -cp splitminer.jar:./lib/* au.edu.unimelb.services.ServiceProvider SMPN {parallelism_threshold} {frequency_threshold}\
    {remove_or_joins} {log_path} {model_destination}"
    print(command)
    result = subprocess.run(
        f"{command}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    print("Output:")
    output = result.stdout
    error = result.stderr
    print(output)

    if len(error) == 0:
        print(f"Success: model stored to {model_destination}")

    file_dest = model_destination + ".pnml"
    net, im, fm = pm4py.read.read_pnml(file_dest)
    return (net, im, fm)


discover_petri_net_split("hi1.xes", "./hello2")
