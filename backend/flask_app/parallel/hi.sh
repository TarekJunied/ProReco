#!/usr/local_rwth/bin/zsh
#SBATCH --ntasks=8
#SBATCH --time=12:00:00
#SBATCH --job-name=TEST
#SBATCH --mem=10G
#SBATCH --output=./parallel_outputs/TEST_OUTPUT.txt
#SBATCH --error=./parallel_outputs/TEST_ERROR.txt
#SBATCH --account=thes1569
#SBATCH --nodes=1
echo "Now starting TEST" 
/usr/bin/python3.9 init.py "/home/qc261227/Recommender/RecommenderSystem/backend/logs/modified_eventlogs" 
