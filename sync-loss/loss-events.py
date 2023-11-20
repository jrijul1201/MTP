import os
import sys


def decrease_by_half(new_val, prev_val):
    return ("--half" in sys.argv) and new_val <= prev_val * 0.5


def decrease_by_one(new_val, prev_val):
    return ("--one" in sys.argv) and new_val < prev_val


def read_data_from_file(input_file_path):
    try:
        with open(input_file_path, "r") as input_file:
            lines = input_file.readlines()
        return lines
    except FileNotFoundError:
        print(f"Error: Input file '{input_file_path}' not found.")
        sys.exit(1)


def parse_data(lines):
    timestamps = []
    values = []

    # Parse the data
    for line in lines:
        try:
            time, value = map(float, line.split())
            timestamps.append(time)
            values.append(value)
        except ValueError:
            print(f"Error: Invalid data format in line '{line}'.")
            sys.exit(1)

    return timestamps, values


def find_selected_timestamps(timestamps, values, input_file_path):
    selected_timestamps = [
        (os.path.splitext(os.path.basename(input_file_path))[0], timestamps[i])
        for i in range(1, len(values))
        if (
            decrease_by_half(values[i], values[i - 1])
            or decrease_by_one(values[i], values[i - 1])
        )
    ]
    return selected_timestamps


def write_selected_timestamps(output_file_path, selected_timestamps):
    with open(output_file_path, "a") as output_file:
        for basename, timestamp in selected_timestamps:
            output_file.write(f"{basename} {timestamp}\n")


def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) == 4:
        input_file_path = sys.argv[1]
        output_file_path = sys.argv[2]

        # Read data from the input file
        lines = read_data_from_file(input_file_path)

        # Parse the data
        timestamps, values = parse_data(lines)

        # Find timestamps meeting the criteria
        selected_timestamps = find_selected_timestamps(
            timestamps, values, input_file_path
        )

        # Write selected timestamps to the output file
        write_selected_timestamps(output_file_path, selected_timestamps)

    else:
        print("Usage: python script.py input_file output_file")
        sys.exit(1)


if __name__ == "__main__":
    main()
