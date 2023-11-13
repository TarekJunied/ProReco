#!/bin/bash
#SBATCH --job-name=propertraining_200traininglogs
#SBATCH --output=training.txt
#SBATCH --error=error_training.txt
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --mem=10G
#SBATCH --account=thes1569
#SBATCH --time=12:00:00


start_time=$(date +"%Y-%m-%d %H:%M:%S")

# Your job commands here
# For example, running your Python script
/usr/bin/python3.9 init.py

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