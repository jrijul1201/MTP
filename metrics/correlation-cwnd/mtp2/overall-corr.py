import pandas as pd
import sys

if len(sys.argv) != 3:
    print("Usage: python script.py input_file output_file")
    sys.exit(1)

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

# Read data from input file
try:
    df = pd.read_csv(input_file_path, delim_whitespace=True, usecols=range(1, 61))
except FileNotFoundError:
    print("Input file not found.")
    sys.exit(1)

# Compute correlation matrix
correlation_matrix = df.corr()

# Extract correlation coefficients
correlation_coefficients = correlation_matrix.values

# Compute overall correlation
overall_correlation = correlation_coefficients.mean()

# Append overall correlation to output file
try:
    with open(output_file_path, "a") as output_file:
        output_file.write(input_file_path + "\t" + str(overall_correlation) + "\n")
    print("Overall correlation appended to output file.")
except FileNotFoundError:
    print("Output file not found.")
    sys.exit(1)
