#!/usr/bin/zsh

### Start of Slurm SBATCH definitions
# ask for eight tasks
#SBATCH --nodes=1
#SBATCH --time=04:00:00


# Ask for less than 4 GB memory per (cpu) task=MPI rank
#SBATCH --mem-per-cpu=3900M

# Name the job
#SBATCH --job-name=ReadLogsAndModels

# Declare file where the STDOUT/STDERR outputs will be written
#SBATCH --output=./outputs/output.%J.txt

PYTHON_SCRIPT="recommender.py"

for NODE in $(scontrol show hostnames); do
    scp ${PYTHON_SCRIPT} ${NODE}:~/
done

echo "Now starting program"
srun -N ${SLURM_NNODES} -n ${SLURM_NNODES} /usr/bin/python3.9 ~/${PYTHON_SCRIPT}