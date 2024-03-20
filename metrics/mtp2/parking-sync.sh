#!/bin/bash

# List of folder paths
folder_paths=(
    "/media/rijul/Seagate Expansion Drive/MTP/MTP2-MidSem/parking-lot/WithoutThresh/60-TcpNewReno-10"
    "/media/rijul/Seagate Expansion Drive/MTP/MTP2-MidSem/parking-lot/WithoutThresh/60-TcpNewReno-200"
    "/media/rijul/Seagate Expansion Drive/MTP/MTP2-MidSem/parking-lot/WithThresh/60-TcpNewReno-10"
    "/media/rijul/Seagate Expansion Drive/MTP/MTP2-MidSem/parking-lot/WithThresh/60-TcpNewReno-200"
)

my_script="parking-sync.py"

# Iterate over folder paths
for folder_path in "${folder_paths[@]}"; do
    echo "Processing ${folder_path}"
    python "$my_script" "$folder_path/cwndTraces"
    echo "${folder_path} done"
done
