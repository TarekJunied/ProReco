import os
import time
import subprocess
from filehelper import gather_all_xes

def generate_job_script(jobscript_path,number_of_tasks,outputs_path,code_to_execute_path,job_name):
    script="#!/usr/bin/zsh\n"
    script+=f"#SBATCH --ntasks={number_of_tasks}\n"
    script+="#SBATCH --time=10:00:00\n"
    script+=f"#SBATCH --array=0-{number_of_tasks-1}\n"
    script+=f"#SBATCH --mem-per-cpu=5000M\n"
    script+=f"#SBATCH --job-name={job_name}\n"
    script+=f"#SBATCH --output={outputs_path}/output_%a.txt\n"
    script+=f"echo \"Now starting {job_name}\" \n"
    script+=f"/usr/bin/python3.9 {code_to_execute_path} $SLURM_ARRAY_TASK_ID {number_of_tasks}\n"


    with open(jobscript_path, 'w') as file:
        file.write(script)
    
def find_text_files(directory):
    text_files = []
    
    # Iterate through all files and subdirectories in the specified directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                # Create the full path to the text file and append it to the list
                text_file_path = os.path.join(root, file)
                text_files.append(text_file_path)
    
    return text_files



def get_status_of_output(output_file):
    try:
        with open(output_file, 'r') as file:
            content = file.read().lower()
            
            if "code 23092002" in content:
                return "DONE"
            elif "error" in content or "err" in content or "errno" in content:
                return "ERROR"
            else:
                return "WORKING"
    except FileNotFoundError:
        return "FILE NOT FOUND"



# Call the function to print the newest file in the folder
def execute_parallel_with_multiple_jobs(jobscript_path,number_of_tasks,outputs_path,code_to_execute_path,job_name):


    generate_job_script(jobscript_path,number_of_tasks,outputs_path,code_to_execute_path,job_name)

    try:
        subprocess.run(['sbatch', jobscript_path], check=True)
        print("Job submitted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error submitting job: {e}")


def print_lines_around_error(filename, error_keyword):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return
    
    error_lines = []
    for i, line in enumerate(lines):
        if error_keyword.lower() in line.lower():
            error_lines.append(i)

    if not error_lines:
        print(f"No lines containing '{error_keyword}' found.")
        return

    for line_num in error_lines:
        start_line = max(0, line_num - 5)
        end_line = min(len(lines), line_num + 6)
        print(f"Lines around '{error_keyword}' in {filename}, line {line_num + 1}:")
        for i in range(start_line, end_line):
            print(f"{i + 1}: {lines[i].strip()}")


def start_monitoring(outputs_path):

    output_files_list = find_text_files(outputs_path)
    cur_no_fertig_tasks = 0
    cur_no_error_tasks = 0
    number_of_tasks = -1


    while cur_no_fertig_tasks != number_of_tasks:
    
        list_of_error = []
        output_files_list = sorted(find_text_files(outputs_path))
        cur_no_fertig_tasks = 0
        cur_no_error_tasks = 0
        number_of_tasks = len(output_files_list)
        
        for output_file in output_files_list:
            print(f"Output file: {output_file}")
            status = get_status_of_output(output_file)
            print(f"STATUS: {status}")
            if status == "DONE":
                cur_no_fertig_tasks += 1
            if status == "ERROR":
                cur_no_error_tasks += 1
                list_of_error += [output_file]
                os.system("clear")
                """"
                print_lines_around_error(output_file,"error")
                print_lines_around_error(output_file,"err")
                print_lines_around_error(output_file,"errno")
                time.sleep(30)
                """
        
        print("Summary:")
        print("Total done: ", cur_no_fertig_tasks)
        print("Out of: ", number_of_tasks)
        print("Errors: ", cur_no_error_tasks)
        for error_file in list_of_error:
            print(error_file)
        time.sleep(20)
        os.system('clear')


n = len(gather_all_xes("../logs/Process_Discovery_Contests/training"))
execute_parallel_with_multiple_jobs("./training_script.sh",80,"./real_output","training.py","procdisc")
start_monitoring("./training_output")