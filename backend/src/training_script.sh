#!/usr/bin/zsh
#SBATCH --ntasks=90
#SBATCH --time=04:00:00
#SBATCH --array=0-89
#SBATCH --mem-per-cpu=5000M
#SBATCH --job-name=test
#SBATCH --output=./training_output/output_%a.txt
echo "Now starting test" 
/usr/bin/python3.9 training.py $SLURM_ARRAY_TASK_ID 90
