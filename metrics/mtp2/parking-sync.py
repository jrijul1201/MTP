import numpy as np
import pandas as pd
import sys
import re
import os
from tqdm import tqdm
import csv


def replace_none_with_first_non_none(arr):
    # Find the first non-None value
    first_non_none = next((value for value in arr if value is not None), None)

    # Replace None with the first non-None value
    filled_array = [first_non_none if value is None else value for value in arr]

    return filled_array


def fill_time_gaps(data):
    filled_data = []

    # Define the time range with a step of 0.1
    time_range = [
        round(175.001 + i * 0.001, 3)
        for i in range(int((199.999 - 175.001) / 0.001) + 1)
    ]

    # Initialize the last known value
    last_value = None

    # Iterate through the time range and fill the gaps
    for time_point in time_range:
        # Check if the time_point exists in the original data
        if any(entry["time"] == time_point for entry in data):
            # If yes, update the last known value
            last_value = next(
                entry["value"] for entry in data if entry["time"] == time_point
            )
        # Append the time and value to the filled data
        filled_data.append(last_value)

    return replace_none_with_first_non_none(filled_data)


def get_matching_files(folder_path, pattern):
    matching_files = []

    # List all files in the folder
    files = os.listdir(folder_path)

    # Filter files based on the specified pattern
    for file in files:
        match = re.match(pattern, file)
        if match:
            matching_files.append(os.path.join(folder_path, file))

    return matching_files


def read_data_from_file(input_file_path):
    try:
        with open(input_file_path, "r") as input_file:
            lines = input_file.readlines()
        return lines
    except FileNotFoundError:
        print(f"Error: Input file '{input_file_path}' not found.")
        sys.exit(1)


def parse_data(lines):
    parsed_data = []

    # Parse the data
    for line in lines:
        try:
            time, value = map(float, line.split())
            parsed_data.append({"time": time, "value": value})
        except ValueError:
            print(f"Error: Invalid data format in line '{line}'.")
            sys.exit(1)

    return parsed_data


def save_matrix_to_csv(matrix, csv_file_path):
    with open(csv_file_path, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        for row in matrix:
            writer.writerow(row)

    print(f"Matrix saved to: {csv_file_path}")


def get_synchrony(traces, set_name):
    df = pd.DataFrame(traces).T

    # print(df)
    # Calculate standard deviation for each column (node)
    sum_sigma_x_i = df.std().sum()  # Sum of standard deviations for each column

    x_tau = df.sum(axis=1)

    sigma_x_tau_squared = x_tau.var()

    phi = sigma_x_tau_squared / (sum_sigma_x_i**2)

    print(input_file_path + "/" + set_name + ": ")
    print(phi)


if len(sys.argv) != 2:
    print("Usage: python script.py input_file")
    sys.exit(1)

cwnd_traces = []
input_file_path = sys.argv[1]
# input_file_path = "/media/rijul/Seagate Expansion Drive/MTP/MTP2-MidSem/parking-lot/WithThresh/60-TcpNewReno-200/cwndTraces"

file_name_pattern = r"n(\d+).dat"  # Assumes names like n1.dat, n2.dat, etc.

# Get the matching files
matching_files = get_matching_files(input_file_path, file_name_pattern)

# Iterate over the matching files
for file_path in tqdm(matching_files, desc="Processing files", unit="file"):
    # Read data from the input file
    lines = read_data_from_file(file_path)
    # Parse the data
    parsed_data = parse_data(lines)
    values = fill_time_gaps(parsed_data)
    cwnd_traces.append(values)

a, b, c = np.array_split(cwnd_traces, 3)

get_synchrony(a, "A")
get_synchrony(b, "B")
get_synchrony(c, "C")
