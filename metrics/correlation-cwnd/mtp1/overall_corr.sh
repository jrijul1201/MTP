#!/bin/bash

# List of folder paths
folder_paths=(
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-sandwich-single/results-sandwich/60-TcpNewReno-10-withoutThresh"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-sandwich-single/results-sandwich/60-TcpNewReno-10-withThresh"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-sandwich-single/results-sandwich/60-TcpNewReno-200-withoutThresh"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-sandwich-single/results-sandwich/60-TcpNewReno-200-withThresh"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-parking-100-100/results-sandwich/WithoutThresh/60-TcpNewReno-10"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-parking-100-100/results-sandwich/WithThresh/60-TcpNewReno-10"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-parking-100-100/results-sandwich/WithoutThresh/60-TcpNewReno-200"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-parking-100-100/results-sandwich/WithThresh/60-TcpNewReno-200"
    # Add more folder paths as needed
)

# Path to the correlation_cwnd.py script
script="overall_corr.py"
file_name="cwndTracescorr_mat.csv"

# Iterate over folder paths
for folder_path in "${folder_paths[@]}"; do
    # Run correlation_cwnd.py on each folder
    echo "Processing ${folder_path}"
    python "$script" "$folder_path/$file_name"
    echo "${folder_path} done"
done
