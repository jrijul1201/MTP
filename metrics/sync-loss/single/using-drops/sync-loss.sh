#!/bin/bash

# Specify the folder path
folder_paths=(
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/4-TcpNewReno-100-withThresh"
)

filename="lossEvents.dat"

for folder_path in "${folder_paths[@]}"; do
    # Log processing completion
    output_file_path="${folder_path}/${filename}"
    python3 compute-sync-metric.py "${output_file_path}" "${folder_path}"
    echo "Processed $folder_path"
done