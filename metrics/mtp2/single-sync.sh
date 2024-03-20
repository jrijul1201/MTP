#!/bin/bash

# List of folder paths
folder_paths=(
    "/media/rijul/Seagate Expansion Drive/MTP/MTP2-MidSem/single/single-bottleneck-withoutThresh/60-TcpNewReno-10"
    "/media/rijul/Seagate Expansion Drive/MTP/MTP2-MidSem/single/single-bottleneck-withThresh/60-TcpNewReno-10"
    "/media/rijul/Seagate Expansion Drive/MTP/MTP2-MidSem/single/single-bottleneck-withoutThresh/60-TcpNewReno-200"
    "/media/rijul/Seagate Expansion Drive/MTP/MTP2-MidSem/single/single-bottleneck-withThresh/60-TcpNewReno-200"
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
