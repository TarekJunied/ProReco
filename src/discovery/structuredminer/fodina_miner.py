import subprocess
import pm4py


def discover_petri_net_fodina(log_path, model_name, timeout_minutes=2):

    command = f"java -jar StructuredMiner.jar fo {str(timeout_minutes)} {log_path} {model_name}"
    print(command)
    result = subprocess.run(
        f"{command}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    print("Output:")
    output = result.stdout
    error = result.stderr
    print(output)

    if len(error) == 0:
        print(f"Success: model stored to ./{model_name}.bpmn")

    bpmn = pm4py.read.read_bpmn(f"{model_name}.bpmn")
    net, im, fm = pm4py.convert_to_petri_net(bpmn)
    pm4py.vis.view_petri_net(net, im, fm)
    return (net, im, fm)


discover_petri_net_fodina("./temp.xes", "new_man")
