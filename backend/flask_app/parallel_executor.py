import os
import time
import subprocess
from filehelper import gather_all_xes


def generate_job_script(job_name, jobscript_path, number_of_tasks, outputs_path, execution_command, execution_time_string="12:00:00"):
    script = "#!/usr/local_rwth/bin/zsh\n"
    script += f"#SBATCH --ntasks={number_of_tasks}\n"
    script += f"#SBATCH --time={execution_time_string}\n"
    script += f"#SBATCH --job-name={job_name}\n"
    script += f"#SBATCH --mem=10G\n"
    script += f"#SBATCH --output={outputs_path}/{job_name}_OUTPUT.txt\n"
    script += f"#SBATCH --error={outputs_path}/{job_name}_ERROR.txt\n"
    script += f"#SBATCH --account=thes1569\n"
    script += f"#SBATCH --nodes=1\n"
    script += f"echo \"Now starting {job_name}\" \n"
    script += f"{execution_command}\n"

    with open(jobscript_path, 'w') as file:
        file.write(script)


execution_command = "/usr/bin/python3.9 init.py \"/home/qc261227/Recommender/RecommenderSystem/backend/logs/modified_eventlogs\" "
generate_job_script("TEST", "./parallel/hi.sh", "8", "./parallel_outputs",
                    execution_command, "12:00:00")
