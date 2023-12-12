#!/bin/bash

# Specify the folder path
folder_paths=(
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-loss-sync/results-sandwich/single-bottleneck-dumbbell-topology/WithoutThresh/60-TcpCubic-10"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-loss-sync/results-sandwich/single-bottleneck-dumbbell-topology/WithoutThresh/60-TcpCubic-200"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-loss-sync/results-sandwich/single-bottleneck-dumbbell-topology/WithoutThresh/60-TcpNewReno-10"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-loss-sync/results-sandwich/single-bottleneck-dumbbell-topology/WithoutThresh/60-TcpNewReno-200"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-loss-sync/results-sandwich/single-bottleneck-dumbbell-topology/WithThresh/60-TcpCubic-10"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-loss-sync/results-sandwich/single-bottleneck-dumbbell-topology/WithThresh/60-TcpCubic-200"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-loss-sync/results-sandwich/single-bottleneck-dumbbell-topology/WithThresh/60-TcpNewReno-10"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-loss-sync/results-sandwich/single-bottleneck-dumbbell-topology/WithThresh/60-TcpNewReno-200"
)

filename="lossEvents.dat"

for folder_path in "${folder_paths[@]}"; do
    # Log processing completion
    output_file_path="${folder_path}/${filename}"
    echo "Processing $output_file_path:"
    if [ -e "$output_file_path" ]; then
        python3 compute-sync-metric.py "${output_file_path}" "${folder_path}"
    else
        echo "0 loss events"
        # echo "File not found: $output_file_path"
    fi
done