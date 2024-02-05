#!/bin/bash

# Assuming the Python script is named makePlots.py
python_script="plot-afct.py"
# Get the list of folders in the specified directory /home/mic/ns-allinone-3.36.1/ns-3.36.1/examples/results/afct/4-TcpNewReno-10-withoutThresh
main_folder="/home/mic/ns-allinone-3.36.1/ns-3.36.1/examples/results/afct-100"
# folders=($(ls -d ${main_folder}/*))
folders=($(ls -d ${main_folder}/*))

# Iterate over each folder and execute the Python script
for folder in "${folders[@]}"; do
    # Extract folder name from the path
    folder_name=$(basename "${folder}")
    mkdir -p ${folder}/plots/
    
    echo "Processing ${folder}"
    # Run the Python script with the folder name as an argument
    python3 "${python_script}" "${folder}" "${folder_name}"
    
    echo "${folder} done"
done