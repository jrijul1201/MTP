import pandas as pd
import numpy as np
import sys


if len(sys.argv) != 2:
    print("Usage: python script.py input_file")
    sys.exit(1)

file_path = sys.argv[1]

# Load the correlation matrix from the CSV file
correlation_matrix = pd.read_csv(file_path, header=None)


# Function to calculate average correlation
def calculate_average_correlation(correlation_matrix):
    n = correlation_matrix.shape[0]

    # Exclude diagonal elements (which are always 1)
    correlations = [
        correlation_matrix.iloc[i, j] for i in range(n) for j in range(n) if i != j
    ]

    # Calculate average correlation
    avg_correlation = sum(correlations) / len(correlations)

    return avg_correlation


# Calculate and print the average correlation
average_correlation = calculate_average_correlation(correlation_matrix)
print(f"Average Correlation: {average_correlation:.4f}")
