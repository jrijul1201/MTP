#!/bin/bash

# List of folder paths
folder_paths=(
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/single-sync/60-TcpNewReno-10-withoutThresh"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/single-sync/60-TcpNewReno-10-withThresh"
)

# Path to the single-sync.py script
my_script="single-sync.py"

# Iterate over folder paths
for folder_path in "${folder_paths[@]}"; do
    # Run single-sync.py on each folder
    echo "Processing ${folder_path}"
    python "$my_script" "$folder_path/cwndTraces"
    echo "${folder_path} done"
done
