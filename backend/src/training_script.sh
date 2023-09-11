#!/usr/bin/zsh
#SBATCH --ntasks=80
#SBATCH --time=10:00:00
#SBATCH --array=0-79
#SBATCH --mem-per-cpu=5000M
#SBATCH --job-name=procdisc
#SBATCH --output=./real_output/output_%a.txt
echo "Now starting procdisc" 
/usr/bin/python3.9 training.py $SLURM_ARRAY_TASK_ID 80
