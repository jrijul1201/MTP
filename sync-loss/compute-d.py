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
        node_int = int(node[1:])
        data_dict[float(timestamp)].append(node_int)

    return data_dict


def compute_d(data_dict):
    # Initialize an empty dictionary to store the mapping of xi to its corresponding index i
    xi_to_i = {}

    # Initialize the 2D array with zeros
    d = []

    # Process each timestamp in the data_dict
    for timestamp, nodes in sorted(data_dict.items()):
        # Iterate over nodes for each timestamp
        for node in nodes:
            # If node is not present in the dictionary, assign a new index to it
            if node not in xi_to_i:
                xi_to_i[node] = len(xi_to_i)

            # Set the corresponding element in the 2D array to 1
            while len(d) <= xi_to_i[node]:
                d.append([0] * T)
            d[xi_to_i[node]][int(timestamp)] = 1

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
    # Step 1: Compute the maximum value in the synchronization matrix
    s_max = max(max(row) for row in s)

    # Step 2: Normalize the synchronization matrix
    normalized_s = [[s_ij / s_max for s_ij in row] for row in s]

    # Step 3: Sum all elements in the normalized synchronization matrix
    total_synchronization = sum(sum(row) for row in normalized_s)

    return total_synchronization


input_file_path = sys.argv[1]
data_dict = consolidate(input_file_path)
T = len(data_dict)
D = compute_d(data_dict)
N = compute_n(D)
NN = compute_nn(D)
S = compute_s(N, NN)
overall_s = overall_synchronization(S)

print(f"Overall synchronisation: {overall_s}")
