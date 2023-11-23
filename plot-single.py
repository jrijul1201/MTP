import os
import random
import sys

import matplotlib.pyplot as plt
import pandas as pd

# absolute_path = input("Enter the name of the folder: ")
absolute_path = sys.argv[1]

labels = ["A", "B", "C"]

queueSizes = ["Queue 1", "Queue 2"]
plot_path = absolute_path + "/plots"

cwnd_folder = absolute_path + "/cwndTraces"

_, axs = plt.subplots(1, 3, figsize=(21, 5))


def reduce_array(arr, arrX, target_difference):
    reduced_array = [arr[0]]  # Start with the first element
    reduced_x = [arrX[0]]

    for i in range(1, len(arr)):
        if arr[i] - reduced_array[-1] >= target_difference:
            reduced_array.append(arr[i])
            reduced_x.append(arrX[i])

    return reduced_array, reduced_x


def plotAndSaveGraph(my_axs, xValues, yValues, label, title, xLabel, yLabel, filepath):
    for i in range(len(xValues)):
        my_axs.plot(xValues[i], yValues[i], label=label[i])
    my_axs.set_xlabel(xLabel)
    my_axs.set_ylabel(yLabel)
    my_axs.set_title(title)
    # my_axs.legend()
    # my_axs.savefig(filepath)
    # my_axs.close()


def readDatFileAndConvertToDataFrame(path, baseName):
    df = pd.read_csv(path, delimiter=" ", header=None)
    return df, plot_path + "/" + baseName + ".png"


# plot cwnd traces

xValues = []
yValues = []

routerPaths = [
    # absolute_path + "/router0/queueSize.dat",
    # absolute_path + "/router1/queueSize.dat",
    absolute_path
    + "/queue-size.dat",
]


def plotQueues():
    xValues = []
    yValues = []
    for queueSizePath in routerPaths:
        df, path = readDatFileAndConvertToDataFrame(queueSizePath, "")
        reducexX, reducedY = df[0], df[1]
        xValues.append(reducexX)
        yValues.append(reducedY)
    plotAndSaveGraph(
        axs[1],
        xValues,
        yValues,
        queueSizes,
        "Queue size vs Time(s)",
        "Time (s)",
        "Queue size",
        plot_path + "/queueSize.png",
    )


def plotCwnds():
    dirList = os.listdir(cwnd_folder)

    random_integers = random.sample(range(0, len(dirList)), 8)

    # Divide the array into three parts
    for i in random_integers:
        filename = dirList[i]
        file_path = os.path.join(cwnd_folder, filename)
        baseName = filename.split(".")
        if baseName[1] != "dat":
            continue
        df, path = readDatFileAndConvertToDataFrame(file_path, baseName[0])
        reducedX, reducedY = df[0], df[1]
        xValues.append(reducedX)
        yValues.append(reducedY)

    for i in range(len(xValues)):
        currLabel = 0
        axs[0].plot(
            xValues[i],
            yValues[i],
            label=labels[currLabel],
            linestyle="-",
        )

    axs[0].set_xlabel("Time (s)")
    axs[0].set_ylabel("Cwnd")
    axs[0].set_title("Cwnd of randomly chosen 8 nodes from each set")


fileName = "throughput.dat"

xValues = []
yValues = []

file_path = os.path.join(absolute_path, fileName)
# print(basename, basename[0], constants[i])
df, path = readDatFileAndConvertToDataFrame(file_path, fileName)
reduxedX, reducedY = reduce_array(df[0], df[1], 0.2)
xValues.append(reduxedX)
yValues.append(reducedY)

plotAndSaveGraph(
    axs[2],
    xValues,
    yValues,
    labels,
    "Average throughput vs Time",
    "Time (s)",
    "Average Throughput (Mbps)",
    plot_path + "/throughput.png",
)


plotCwnds()

plotQueues()

# Adjust layout for better spacing
plt.tight_layout()

# Save the final figure
plt.savefig(plot_path + "/combined_plots.png")
