#!/bin/bash

# Parent folder path
parent_folder="/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-FinalResult"

# Path to the sync-metric.py script
script="sync-metric.py"
process_script="process-for-tikz.py"

# Output file name
output_file_name="sync-matric.txt"

# Get a list of child folders inside the parent folder
child_folders=("$parent_folder"/*)

# Iterate over child folders
for folder_path in "${child_folders[@]}"; do
    # Check if the folder exists and is a directory
    if [[ -d "$folder_path" ]]; then
        echo "Processing $folder_path"
        
        # Output file name with folder name appended
        folder_name=$(basename "$folder_path")
        output_file="$folder_path/$folder_name-$output_file_name"
        
        rm -f $output_file
        touch -f $output_file
        
        # Run the script for files containing "cwnd" in their names
        for file in "$folder_path"/*cwnd*; do
            if [[ -f "$file" ]]; then
                echo "Running script for $file"
                python "$script" "$file" "$output_file" "$folder_name"
            fi
        done
        
        python "$process_script" "$output_file"
        echo "Processing $folder_path done"
    fi
done