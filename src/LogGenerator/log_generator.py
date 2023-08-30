import subprocess
import datetime


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
        print(f"Success: process stored to {storage_path}")
    else:
        print("An error has occured.")
        print("Errors:")ç
        print(error)


process_path = create_random_process()
for i in range(100):
    create_log_from_model(process_path, 100)
