#!/bin/bash

# Specify the folder path
folder_paths=(
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-loss-sync/results-sandwich/parking-lot-topology/WithoutThresh/60-TcpCubic-10"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-loss-sync/results-sandwich/parking-lot-topology/WithoutThresh/60-TcpCubic-200"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-loss-sync/results-sandwich/parking-lot-topology/WithoutThresh/60-TcpNewReno-10"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-loss-sync/results-sandwich/parking-lot-topology/WithoutThresh/60-TcpNewReno-200"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-loss-sync/results-sandwich/parking-lot-topology/WithThresh/60-TcpCubic-10"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-loss-sync/results-sandwich/parking-lot-topology/WithThresh/60-TcpCubic-200"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-loss-sync/results-sandwich/parking-lot-topology/WithThresh/60-TcpNewReno-10"
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/results-loss-sync/results-sandwich/parking-lot-topology/WithThresh/60-TcpNewReno-200"
)

router_folders=("router0" "router1")
filename_losses=("lossEvents0.dat" "lossEvents1.dat" "lossEvents2.dat")

for folder_path in "${folder_paths[@]}"; do
    for router_folder in "${router_folders[@]}"; do
        for filename_loss in "${filename_losses[@]}"; do
            output_file_path="${folder_path}/${router_folder}/${filename_loss}"
            
            # Check if the file exists
            echo "Processing $output_file_path:"
            if [ -e "$output_file_path" ]; then
                # Log processing completion
                python3 compute-sync-metric.py "${output_file_path}" "${folder_path}/${router_folder}"
            else
                echo "0 loss events"
                # echo "File not found: $output_file_path"
            fi
        done
    done
done