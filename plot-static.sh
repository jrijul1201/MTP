#!/bin/bash

# Assuming the Python script is named makePlots.py
python_script="plot-static.py"
# Get the list of folders in the specified directory
main_folder="/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/static-routing-via-virtual"
folders=($(ls -d ${main_folder}/*/*))

# Iterate over each folder and execute the Python script
for folder in "${folders[@]}"; do
    # Extract folder name from the path
    folder_name=$(basename "${folder}")
    mkdir -p ${folder}/plots/
    
    echo "Processing ${folder}"
    # Run the Python script with the folder name as an argument
    python "${python_script}" "${folder}"
    
    echo "${folder} done"
done