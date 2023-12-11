import csv
import math
import os
import sys
from collections import defaultdict


def consolidate(input_file_path):
    # Read the data from the original .dat file
    with open(input_file_path, "r") as file:
        lines = file.readlines()

    # Parse the data and group it by timestamp
    data_dict = defaultdict(list)
    for line in lines:
        node, timestamp = line.split()
        node_int = int(node)
        data_dict[float(timestamp)].append(node_int)

    return data_dict


def compute_d(data_dict):
    # Initialize an empty dictionary to store the mapping of xi to its corresponding index i
    xi_to_i = {}

    # Initialize the 2D array with zeros
    d = []

    # Initialize the running index i
    i = 0

    # Process each timestamp in the data_dict
    for _, nodes in sorted(data_dict.items()):
        # Iterate over nodes for each timestamp
        for node in nodes:
            # If node is not present in the dictionary, assign a new index to it
            if node not in xi_to_i:
                xi_to_i[node] = len(xi_to_i)

            # Set the corresponding element in the 2D array to 1
            while len(d) <= xi_to_i[node]:
                d.append([0] * T)  # Use the running index i
            d[xi_to_i[node]][i] = 1

        i += 1

    # for row in d:
    #     print(row)

    return d


# n is the list of Ni
def compute_n(d):
    n = []
    for row in d:
        Nk = sum(row)
        n.append(Nk)

    # print(n)

    return n


# nn is the matrix of Nij
def compute_nn(d):
    n_nodes = len(d)
    nn = [
        [sum(d[i][l] * d[j][l] for l in range(len(d[0]))) for j in range(n_nodes)]
        for i in range(n_nodes)
    ]

    # for row in nn:
    #     print(row)

    return nn


# sij is  nij/ min(ni, nj)
def compute_s(n, nn):
    n_nodes = len(n)
    s = [[nn[i][j] / min(n[i], n[j]) for j in range(n_nodes)] for i in range(n_nodes)]

    # for row in nn:
    #     print(row)

    return s


def overall_synchronization(s):
    if not any(s):
        return 0.0
    # Step 1: Compute the maximum value in the synchronization matrix
    s_max = max(max(row) for row in s)

    # Step 2: Normalize the synchronization matrix
    normalized_s = [[s_ij / s_max for s_ij in row] for row in s]

    # Step 3: Sum all elements in the normalized synchronization matrix
    total_synchronization = sum(sum(row) for row in normalized_s)

    return total_synchronization


def save_s_matrix_to_csv(s_matrix, csv_file_path):
    with open(csv_file_path, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        for row in s_matrix:
            writer.writerow(row)

    # print(f"S matrix saved to: {csv_file_path}")


def frobenius_norm(s):
    return math.sqrt(sum(sum(x**2 for x in row) for row in s))


input_file_path = sys.argv[1]
folder_path = sys.argv[2]
mode_of_calculation = sys.argv[3]
data_dict = consolidate(input_file_path)
T = len(data_dict)
D = compute_d(data_dict)
N = compute_n(D)
NN = compute_nn(D)
S = compute_s(N, NN)
overall_s = overall_synchronization(S)
frob_norm = frobenius_norm(S)
csv_file_path = os.path.join(folder_path, "s_matrix.csv")

save_s_matrix_to_csv(S, csv_file_path)

# print(mode_of_calculation)
# print(f"Overall synchronisation: {overall_s}")
print(f"Frobenius norm: {frob_norm}")
