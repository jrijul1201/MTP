import numpy as np
import sys
import re
import os


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


cwnd_traces = []
input_file_path = input("Enter the name of the folder: ")

file_name_pattern = r"n(\d+).dat"  # Assumes names like n1.dat, n2.dat, etc.

# Get the matching files
matching_files = get_matching_files(input_file_path, file_name_pattern)

# Iterate over the matching files
for file_path in matching_files:
    # Read data from the input file
    lines = read_data_from_file(file_path)
    # Parse the data
    parsed_data = parse_data(lines)
    values = fill_time_gaps(parsed_data)
    cwnd_traces.append(values)

# Initialize an empty correlation matrix
correlation_matrix = np.zeros((len(cwnd_traces), len(cwnd_traces)))

# Calculate correlation coefficient for each pair of traces
for i in range(len(cwnd_traces)):
    for j in range(i + 1, len(cwnd_traces)):
        cwnd_values_i = [trace for trace in cwnd_traces[i]]
        cwnd_values_j = [trace for trace in cwnd_traces[j]]

        correlation_coefficient = np.corrcoef(
            cwnd_values_i, cwnd_values_j, rowvar=False
        )[0, 1]

        correlation_matrix[i, j] = correlation_coefficient
        correlation_matrix[
            j, i
        ] = correlation_coefficient  # Since the matrix is symmetric

# Print or use the correlation matrix as needed
print("Correlation Matrix:")
print(correlation_matrix)
