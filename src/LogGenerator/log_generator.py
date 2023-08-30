import subprocess
import time

command_without_args = "/Library/Java/JavaVirtualMachines/jdk-18.0.1.1.jdk/Contents/Home/bin/java -Dfile.encoding=UTF-8 -classpath /Users/tarekjunied/Documents/Universität/BachelorThesis/src/LogGenerator/PLG/libPlg/bin:/Users/tarekjunied/Documents/Universität/BachelorThesis/src/LogGenerator/PLG/libPlg/lib/jython/jython-standalone-2.5.3.jar:/Users/tarekjunied/Documents/Universität/BachelorThesis/src/LogGenerator/PLG/libPlg/lib/jdom/jdom-2.0.5.jar:/Users/tarekjunied/Documents/Universität/BachelorThesis/src/LogGenerator/PLG/libPlg/lib/multiline-string-0.1.1.jar:/Users/tarekjunied/Documents/Universität/BachelorThesis/src/LogGenerator/PLG/libPlg/lib/commons-io/commons-io-2.4.jar:/Users/tarekjunied/Documents/Universität/BachelorThesis/src/LogGenerator/PLG/libPlg/lib/colt/colt.jar:/Users/tarekjunied/Documents/Universität/BachelorThesis/src/LogGenerator/PLG/libPlg/lib/colt/concurrent.jar:/Users/tarekjunied/Documents/Universität/BachelorThesis/src/LogGenerator/PLG/libPlg/lib/OpenXES/guava-16.0.1.jar:/Users/tarekjunied/Documents/Universität/BachelorThesis/src/LogGenerator/PLG/libPlg/lib/OpenXES/OpenXES-XStream.jar:/Users/tarekjunied/Documents/Universität/BachelorThesis/src/LogGenerator/PLG/libPlg/lib/OpenXES/OpenXES.jar:/Users/tarekjunied/Documents/Universität/BachelorThesis/src/LogGenerator/PLG/libPlg/lib/OpenXES/xpp3_min-1.1.4c.jar:/Users/tarekjunied/Documents/Universität/BachelorThesis/src/LogGenerator/PLG/libPlg/lib/OpenXES/xstream-1.3.1.jar:/Users/tarekjunied/Documents/Universität/BachelorThesis/src/LogGenerator/PLG/libPlg/lib/reflections-0.10-SNAPSHOT.jar:/Users/tarekjunied/Documents/Universität/BachelorThesis/src/LogGenerator/PLG/libPlg/lib/OpenXES/Spex.jar:/Users/tarekjunied/Documents/Universität/BachelorThesis/src/LogGenerator/PLG/libPlg/lib/camunda-bpmn-model-7.5.0.jar -XX:+ShowCodeDetailsInExceptionMessages plg.loggenerator.ProcGenerator"


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

    command = (
        str(command_without_args) + " " +
        str(and_branches) + " " +
        str(xor_branches) + " " +
        str(loop_weight) + " " +
        str(single_activity_weight) + " " +
        str(skip_weight) + " " +
        str(sequence_weight) + " " +
        str(and_weight) + " " +
        str(xor_weight) + " " +
        str(max_depth) + " " +
        str(data_object_probability)
    )

    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # TODO: return path of model as string

    print("Output:")
    print(result.stdout)

    print("Errors:")
    print(result.stderr)


def create_log_from_model(model_path, no_traces=1000):
    command = "java -jar /Users/tarekjunied/Documents/Universität/BachelorThesis/src/LogGenerator/LogGenerator.jar "
    command += "-l" + " " + "./logs/log_" + str(time.time()) + " "
    command += "-m" + " " + model_path + " "
    command += "-c" + " " + str(no_traces) + " "

    print(command)

    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    print("Output:")
    print(result.stdout)

    print("Errors:")
    print(result.stderr)


create_random_process()

# create_log_from_model("/Users/tarekjunied/Documents/Universität/BachelorThesis/src/LogGenerator/processes/process_2023-08-29T19:06:38.961248Z.plg")
