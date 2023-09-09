#!/usr/bin/zsh
#SBATCH --ntasks=14
#SBATCH --time=10:00:00
#SBATCH --array=0-13
#SBATCH --mem-per-cpu=5000M
#SBATCH --job-name=real_logs
#SBATCH --output=./real_output/output_%a.txt
echo "Now starting real_logs" 
/usr/bin/python3.9 recommender.py $SLURM_ARRAY_TASK_ID 14
