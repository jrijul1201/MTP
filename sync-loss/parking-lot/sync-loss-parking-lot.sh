#!/bin/bash

# Function to remove existing file
remove_existing_file() {
    local file_path="$1"
    if [ -e "$file_path" ]; then
        rm "$file_path"
        echo "Existing $(basename "$file_path") removed."
    fi
}

# Specify the folder path
folder_paths=(
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/end-sem-results/WithThresh/60-TcpNewReno-200/cwndTraces"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/end-sem-results/WithoutThresh/60-TcpNewReno-200/cwndTraces"
)
filename_losses=("loss-events0.dat" "loss-events1.dat" "loss-events2.dat")

for filename_loss in "${filename_losses[@]}"; do
    for folder_path in "${folder_paths[@]}"; do
        output_file_path="${folder_path}/${filename_loss}"
        
        # Remove existing files
        # remove_existing_file "$output_file_path"
        
        # Iterate over each file in the folder
        # for file in "$folder_path"/*; do
        #     # Check if the item is a file (not a directory)
        #     if [ -f "$file" ]; then
        #         # Extract the filename without the path
        #         filename=$(basename "$file")
        
        #         # Check if the filename matches the pattern "n{i}.dat"
        #         if [[ $filename =~ ^n[0-9]+\.dat$ ]]; then
        #             # Run loss-events.py script on the current file with complete filepath
        #             python3 loss-events.py "$file" "$output_file_path" --half
        
        #         fi
        #     fi
        # done
        
        # Log processing completion
        echo "Processed $folder_path"
        echo "Processed $output_file_path"
        python3 compute-sync-metric.py "${output_file_path}" "${folder_path}" --half
    done
done