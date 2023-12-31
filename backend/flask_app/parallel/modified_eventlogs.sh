#!/usr/local_rwth/bin/zsh
#SBATCH --job-name=modified_eventlogs
#SBATCH --output=/home/qc261227/Recommender/RecommenderSystem/backend/flask_app/parallel/modified_OUTPUT.txt
#SBATCH --error=/home/qc261227/Recommender/RecommenderSystem/backend/flask_app/parallel/modified_ERROR.txt
#SBATCH --nodes=1
#SBATCH --ntasks=12
#SBATCH --cpus-per-task=4
#SBATCH --mem=10G
#SBATCH --time=72:00:00
#SBATCH --account=thes1569


start_time=$(date +"%Y-%m-%d %H:%M:%S")


/usr/bin/python3.9 init.py "/home/qc261227/Recommender/RecommenderSystem/backend/logs/modified_eventlogs"



# Record the end time
end_time=$(date +"%Y-%m-%d %H:%M:%S")

# Calculate the duration
start_timestamp=$(date -d "$start_time" +"%s")
end_timestamp=$(date -d "$end_time" +"%s")
duration_seconds=$((end_timestamp - start_timestamp))
duration_minutes=$((duration_seconds / 60))

# Save the start time, end time, and duration to the output.txt file
echo "Job started at: $start_time" >> output.txt
echo "Job ended at:   $end_time" >> output.txt
echo "Duration (minutes): $duration_minutes" >> output.txt