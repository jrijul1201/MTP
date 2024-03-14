import sys, os

def read_data_from_file(file_path):
    """
    Reads data from a file and returns it as a list of dictionaries.
    Each dictionary represents a row in the data with keys as column names.
    """
    data = []
    with open(file_path, 'r') as file:
        # Skip the header
        header = file.readline().strip().split()
        # Read each line and convert it into a dictionary
        for line in file:
            line_data = line.strip().split()
            row = {header[i]: float(line_data[i]) for i in range(len(header))}
            data.append(row)
    return data

def write_data_to_file(file_path, data):
    """
    Writes the data to a file.
    """
    with open(file_path, 'w') as file:
        # Write the header
        header = '\t'.join(data[0].keys()) + '\n'
        file.write(header)
        # Write each row of data
        for row in data:
            row_values = '\t'.join(map(str, row.values())) + '\n'
            file.write(row_values)

def sort_data_by_rtt(data):
    """
    Sorts the data by the 'rtt' column in ascending order.
    """
    sorted_data = sorted(data, key=lambda x: x['rtt'])
    return sorted_data

# Example usage:
def sort_data(file_path):
    data = read_data_from_file(file_path)
    sorted_data = sort_data_by_rtt(data)
    write_data_to_file(file_path, sorted_data)

folderPath = "/home/dipesh/Desktop/ns-allinone-3.36.1/ns-3.36.1/examples/results/processed-data/"

for file in os.listdir(folderPath):
    sort_data(folderPath+file)