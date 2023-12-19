#!/bin/bash

# Define the root directory
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

files=("lossEvents0.dat" "lossEvents1.dat" "lossEvents2.dat")

for filename in "${files[@]}"; do
    for root_dir in "${folder_paths[@]}"; do
        file1="${root_dir}/router0/${filename}"
        file2="${root_dir}/router1/${filename}"
        
        # Check if both files exist
        if [ -e "$file1" ] && [ -e "$file2" ]; then
            cat "$file1" "$file2" > "${root_dir}/${filename}"
            elif [ -e "$file1" ]; then
            cp "$file1" "${root_dir}/${filename}"
            elif [ -e "$file2" ]; then
            cp "$file2" "${root_dir}/${filename}"
        else
            # Create an empty file if none exist
            touch "${root_dir}/${filename}"
        fi
    done
done