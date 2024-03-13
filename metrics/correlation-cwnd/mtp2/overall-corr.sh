#!/bin/bash

# Parent folder path
parent_folder="/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-FinalResult"

# Path to the overall-corr.py script
script="overall-corr.py"

# Output file name
output_file_name="cwnd-corr.txt"

# Delete old output file if it exists
rm -f "$parent_folder/$output_file_name"

# Create the output file
touch "$parent_folder/$output_file_name"

# Get a list of child folders inside the parent folder
child_folders=("$parent_folder"/*)

# Iterate over child folders
for folder_path in "${child_folders[@]}"; do
    # Check if the folder exists and is a directory
    if [[ -d "$folder_path" ]]; then
        echo "Processing $folder_path"
        
        # Run the script for files containing "cwnd" in their names
        for file in "$folder_path"/*cwnd*; do
            if [[ -f "$file" ]]; then
                echo "Running script for $file"
                python "$script" "$file" "$parent_folder/$output_file_name"
            fi
        done
        
        echo "Processing $folder_path done"
    fi
done
