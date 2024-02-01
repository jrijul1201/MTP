import os
import random
import sys

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# folder_path = "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/static-routing-via-virtual/WithThresh/146-TcpNewReno-100"

folder_path = sys.argv[1]
plot_path = folder_path + "/plots"

cwnd_folder = folder_path + "/cwndTraces"

routerPaths = [
    "router1",
    "router2",
    "router3",
    "router4",
    "router5",
    "router6",
]

config = "60" if "146" in folder_path else "80"
config += " nodes "
config += "WithThresh" if "WithThresh" in folder_path else "DropTail"


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
    for routerNum in routerPaths:
        df, path = readDatFileAndConvertToDataFrame(
            folder_path + "/" + routerNum + "/queueSize.dat", "queueSize_" + routerNum
        )
        fig, axs = plt.subplots()  # Create a new figure and axis for each plot
        plotAndSaveGraph(
            axs,
            np.array(df[0]),
            np.array(df[1]),
            "Queue -" + routerNum,
            config + " - " + routerNum + " - Queue size vs Time(s)",
            "Time (s)",
            "Queue size",
            path,
        )


# Call the plotQueues function
plotQueues()
