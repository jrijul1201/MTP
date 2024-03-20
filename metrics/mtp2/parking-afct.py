import sys

if len(sys.argv) != 2:
    print("Usage: python script.py input_file")
    sys.exit(1)

input_file_path = sys.argv[1] + "/fct.dat"

# Read data from the file
with open(input_file_path, "r") as file:
    lines = file.readlines()

# Initialize variables to store sums for each set
sum_A = 0
sum_B = 0
sum_C = 0

# Loop through the lines and calculate the sums for each set
for i, line in enumerate(lines[1:]):  # Skip the header line
    flow, fct = line.strip().split("\t")
    fct = float(fct)

    if i < 30:
        sum_A += fct
    elif i < 60:
        sum_B += fct
    else:
        sum_C += fct

# Calculate averages for each set
avg_A = sum_A / 30
avg_B = sum_B / 30
avg_C = sum_C / 30

# Display the results
print("Average FCT for Set A:", avg_A)
print("Average FCT for Set B:", avg_B)
print("Average FCT for Set C:", avg_C)
