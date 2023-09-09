#!/usr/bin/zsh
#SBATCH --ntasks=95
#SBATCH --time=10:00:00
#SBATCH --array=0-94
#SBATCH --mem-per-cpu=5000M
#SBATCH --job-name=real_logs
#SBATCH --output=./training_output/output_%a.txt
echo "Now starting real_logs" 
/usr/bin/python3.9 training.py $SLURM_ARRAY_TASK_ID 95
