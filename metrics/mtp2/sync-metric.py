import pandas as pd
import sys
import os

if len(sys.argv) != 4:
    print("Usage: python script.py input_file output_file folder_name")
    sys.exit(1)

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]
folder_name = sys.argv[3]

# Read data from input file
try:
    df = pd.read_csv(input_file_path, delim_whitespace=True, usecols=range(1, 61))
except FileNotFoundError:
    print("Input file not found.")
    sys.exit(1)

# Extract file name
file_name = os.path.basename(input_file_path)
file_name = file_name.split(folder_name)[1]
file_name = file_name.replace("RTTcwnd.txt", "")
file_name = file_name.replace("ms", "")

# Calculate standard deviation for each column (node)
sum_sigma_x_i = df.std().sum()  # Sum of standard deviations for each column

x_tau = df.sum(axis=1)

sigma_x_tau_squared = x_tau.var()

phi = sigma_x_tau_squared / (sum_sigma_x_i**2)  # Corrected exponentiation operator

# Append overall correlation to output file
try:
    with open(output_file_path, "a") as output_file:
        output_file.write(file_name + "\t" + str(phi) + "\n")
    # print("Overall correlation appended to output file.")
except FileNotFoundError:
    print("Output file not found.")
    sys.exit(1)
