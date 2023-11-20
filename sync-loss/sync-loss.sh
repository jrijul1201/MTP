#!/bin/bash

# Specify the folder path
folder_path="/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/60-TcpNewReno-200-withoutThresh/cwndTraces"
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
        # python3 loss-events.py "$file" --one
        python3 loss-events.py "$file" --half
        
        echo "Processed $file"
    fi
done

echo "Processed $folder_path"
python3 compute-sync-metric.py "${output_file_path}" "${folder_path}"