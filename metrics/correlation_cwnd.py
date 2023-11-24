import numpy as np

# Assuming you have 90 cwnd traces, each represented as a list
cwnd_traces = [
    # Trace 1
    [[175.073, 73], [175.155, 51], [175.609, 52], ...],
    # Trace 2
    [[...], ...],
    # ... (repeat for the remaining 88 traces)
]

# Initialize an empty correlation matrix
correlation_matrix = np.zeros((len(cwnd_traces), len(cwnd_traces)))

# Calculate correlation coefficient for each pair of traces
for i in range(len(cwnd_traces)):
    for j in range(i + 1, len(cwnd_traces)):
        cwnd_values_i = [trace[1] for trace in cwnd_traces[i]]
        cwnd_values_j = [trace[1] for trace in cwnd_traces[j]]

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
