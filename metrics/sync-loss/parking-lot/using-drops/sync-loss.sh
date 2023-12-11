#!/bin/bash

# Specify the folder path
folder_paths=(
    "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/WithoutThresh/10-TcpNewReno-100"
)

router_folders=("router0" "router1")
filename_losses=("lossEvents0.dat" "lossEvents1.dat" "lossEvents2.dat")

for folder_path in "${folder_paths[@]}"; do
    for router_folder in "${router_folders[@]}"; do
        for filename_loss in "${filename_losses[@]}"; do
            output_file_path="${folder_path}/${router_folder}/${filename_loss}"
            
            # Check if the file exists
            if [ -e "$output_file_path" ]; then
                # Log processing completion
                python3 compute-sync-metric.py "${output_file_path}" "${folder_path}/${router_folder}"
            else
                echo "File not found: $output_file_path"
            fi
            echo "Processed $output_file_path"
        done
    done
done