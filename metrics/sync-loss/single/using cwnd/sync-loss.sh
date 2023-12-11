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
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-sandwich-single/results-sandwich/60-TcpNewReno-200-withoutThresh/cwndTraces"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-sandwich-single/results-sandwich/60-TcpNewReno-200-withThresh/cwndTraces"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-sandwich-single/results-sandwich/60-TcpNewReno-10-withoutThresh/cwndTraces"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-sandwich-single/results-sandwich/60-TcpNewReno-10-withThresh/cwndTraces"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-sandwich-single/results-sandwich/60-TcpCubic-200-withoutThresh/cwndTraces"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-sandwich-single/results-sandwich/60-TcpCubic-200-withThresh/cwndTraces"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-sandwich-single/results-sandwich/60-TcpCubic-10-withoutThresh/cwndTraces"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-sandwich-single/results-sandwich/60-TcpCubic-10-withThresh/cwndTraces"
)
# filename_one="loss-events-one.dat"
filename_half="loss-events-half.dat"

for folder_path in "${folder_paths[@]}"; do
    # output_file_path_one="${folder_path}/${filename_one}"
    output_file_path_half="${folder_path}/${filename_half}"
    
    # Remove existing files
    # remove_existing_file "$output_file_path_one"
    remove_existing_file "$output_file_path_half"
    
    # Iterate over each file in the folder
    for file in "$folder_path"/*; do
        # Check if the item is a file (not a directory)
        if [ -f "$file" ]; then
            # Extract the filename without the path
            filename=$(basename "$file")
            
            # Check if the filename matches the pattern "n{i}.dat"
            if [[ $filename =~ ^n[0-9]+\.dat$ ]]; then
                # Run loss-events.py script on the current file with complete filepath
                # python3 loss-events.py "$file" "$output_file_path_one" --one
                python3 loss-events.py "$file" "$output_file_path_half" --half
                
                # echo "Processed $file"
                # else
                # echo "Skipping file $file. Filename does not match the required pattern."
            fi
        fi
    done
    
    # Log processing completion
    echo "Processed $folder_path"
    python3 compute-sync-metric.py "${output_file_path_half}" "${folder_path}" --half
    # python3 compute-sync-metric.py "${output_file_path_one}" "${folder_path}" --one
done