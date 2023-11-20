import os
import sys

# Check if the correct number of command-line arguments is provided
if len(sys.argv) == 2:
    # Get the input file path from the command-line argument
    input_file_path = sys.argv[1]

    # Check if the input file exists
    if not os.path.isfile(input_file_path):
        print(f"Error: Input file '{input_file_path}' not found.")
        sys.exit(1)

    # Generate output file path in the same folder with the fixed name 'loss-events.dat'
    output_file_path = os.path.join(os.path.dirname(input_file_path), "loss-events.dat")

    with open(input_file_path, "r") as input_file:
        lines = input_file.readlines()

    timestamps = []
    values = []

    # Parse the data
    for line in lines:
        time, value = map(float, line.split())
        timestamps.append(time)
        values.append(value)

    # Find timestamps where the new value is less than or equal to half of the previous value
    selected_timestamps = [
        (os.path.splitext(os.path.basename(input_file_path))[0], timestamps[i])
        for i in range(1, len(values))
        if values[i] < values[i - 1]
    ]

    # Write the selected timestamps with basename to the fixed output file in the same folder
    with open(output_file_path, "a") as output_file:
        for basename, timestamp in selected_timestamps:
            output_file.write(f"{basename} {timestamp}\n")