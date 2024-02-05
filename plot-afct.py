import os
import random
import sys

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# folder_path = "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/static-routing-via-virtual/WithThresh/146-TcpNewReno-100"

folder_path = sys.argv[1]
folder_name = sys.argv[2]
plot_path = folder_path + "/plots"

cwnd_folder = folder_path + "/cwndTraces"

def reduce_array(arr, arrX, target_difference):
    reduced_array = [arr[0]]  # Start with the first element
    reduced_x = [arrX[0]]

    for i in range(1, len(arr)):
        if arr[i] - reduced_array[-1] >= target_difference:
            reduced_array.append(arr[i])
            reduced_x.append(arrX[i])

    return reduced_array, reduced_x


def plotAndSaveGraph(my_axs, xValues, yValues, label, title, xLabel, yLabel, filepath):
    my_axs.plot(xValues, yValues, label=label)
    my_axs.set_xlabel(xLabel)
    my_axs.set_ylabel(yLabel)
    my_axs.set_title(title)
    my_axs.figure.savefig(filepath)  # Use figure to save the entire plot
    plt.close()


def readDatFileAndConvertToDataFrame(path, baseName):
    df = pd.read_csv(path, delimiter=" ", header=None)
    return df, plot_path + "/" + baseName + ".png"


def plotQueues():
    # for routerNum in routerPaths:
    df, path = readDatFileAndConvertToDataFrame(
        folder_path + "/queueSize.dat","Queue-size"
    )
    fig, axs = plt.subplots()  # Create a new figure and axis for each plot
    reducexX, reducedY = reduce_array(df[0], df[1], 0.2)
    plotAndSaveGraph(
        axs,
        reducexX,
        reducedY,
        "Queue",
        folder_name+" Queue size vs Time(s)",
        "Time (s)",
        "Queue size",
        path,
    )


# Call the plotQueues function
plotQueues()
