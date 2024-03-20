#!/bin/bash

# List of folder paths
folder_paths=(
    "/media/rijul/Seagate Expansion Drive/MTP/MTP2-MidSem/parking-afct/60-TcpNewReno-10-withThresh"
    "/media/rijul/Seagate Expansion Drive/MTP/MTP2-MidSem/parking-afct/60-TcpNewReno-200-withThresh"
    "/media/rijul/Seagate Expansion Drive/MTP/MTP2-MidSem/parking-afct/60-TcpNewReno-10-withoutThresh"
    "/media/rijul/Seagate Expansion Drive/MTP/MTP2-MidSem/parking-afct/60-TcpNewReno-200-withoutThresh"
)

my_script="parking-afct.py"

# Iterate over folder paths
for folder_path in "${folder_paths[@]}"; do
    echo "Processing ${folder_path}"
    python "$my_script" "$folder_path"
    echo "${folder_path} done"
done
