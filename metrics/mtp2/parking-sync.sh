#!/bin/bash

# List of folder paths
folder_paths=(
    "/home/Dipesh/ns-allinone-3.36.1/ns-3.36.1/examples/results/ppt-parking-lotWithoutThresh/60-TcpNewReno-10"
    "/home/Dipesh/ns-allinone-3.36.1/ns-3.36.1/examples/results/ppt-parking-lotWithThresh/60-TcpNewReno-10"
    "/home/Dipesh/ns-allinone-3.36.1/ns-3.36.1/examples/results/ppt-parking-lotWithThresh/60-TcpNewReno-200"
    "/home/Dipesh/ns-allinone-3.36.1/ns-3.36.1/examples/results/ppt-parking-lotWithoutThresh/60-TcpNewReno-200"
)

my_script="parking-sync.py"

# Iterate over folder paths
for folder_path in "${folder_paths[@]}"; do
    echo "Processing ${folder_path}"
    python "$my_script" "$folder_path/cwndTraces"
    echo "${folder_path} done"
done
