python_script="append-fct-data.py"
# Get the list of folders in the specified directory /home/mic/ns-allinone-3.36.1/ns-3.36.1/examples/results/afct/4-TcpNewReno-10-withoutThresh
main_folder="/home/dipesh/Desktop/ns-allinone-3.36.1/ns-3.36.1/examples/results/mahima"
# folders=($(ls -d ${main_folder}/*))
folders=($(ls -d ${main_folder}/*))

# Iterate over each folder and execute the Python script
for folder in "${folders[@]}"; do
    echo "Processing ${folder}"
    # Run the Python script with the folder name as an argument
    python3 "${python_script}" "${folder}"
    echo "${folder} done"
done

python3 sort-data.py