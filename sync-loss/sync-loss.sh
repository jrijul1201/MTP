#!/bin/bash

# Specify the folder path
folder_path="/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/60-TcpNewReno-10/cwndTraces"
filename="loss-events.dat"
output_file_path="${folder_path}/${filename}"


# Check if the file exists before proceeding
if [ -e "${output_file_path}" ]; then
    # Remove the existing file
    rm "${output_file_path}"
    echo "Existing ${filename} removed."
fi

# Iterate over each file in the folder
for file in "$folder_path"/*; do
    # Check if the item is a file (not a directory)
    if [ -f "$file" ]; then
        # Run loss-events.py script on the current file with complete filepath
        python loss-events.py "$file"
        
        echo "Processed $file"
    fi
done

python3 compute-d.py "${output_file_path}"

echo "Consolidation complete."
echo "D has been computed."