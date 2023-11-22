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
colors = ["#CC0000", "#0066CC", "#339933"]
color_values = [
    "#FF9999",
    "#FF6666",
    "#CC0000",
    "#800000",
    "#66CCFF",
    "#3399FF",
    "#0066CC",
    "#000066",
    "#99FF99",
    "#66FF66",
    "#339933",
    "#006600",
]
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
    my_axs.legend()
    # my_axs.savefig(filepath)
    # my_axs.close()


def readDatFileAndConvertToDataFrame(path, baseName):
    df = pd.read_csv(path, delimiter=" ", header=None)
    return df, plot_path + "/" + baseName + ".png"


# plot cwnd traces

xValues = []
yValues = []

routerPaths = [
    absolute_path + "/router0/queueSize.dat",
    absolute_path + "/router1/queueSize.dat",
]


def plotQueues():
    xValues = []
    yValues = []
    for queueSizePath in routerPaths:
        df, path = readDatFileAndConvertToDataFrame(queueSizePath, "")
        reducexX, reducedY = reduce_array(df[0], df[1], 0.2)
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

    length = len(dirList)
    length = length // 3

    random_integers = [
        i * length + j
        for i in range(0, 3)
        for j in random.sample(range(0, length - 1), 4)
    ]

    legend_labels = ["A", "B", "C"]

    # Divide the array into three parts
    for i in random_integers:
        filename = dirList[i]
        file_path = os.path.join(cwnd_folder, filename)
        baseName = filename.split(".")
        if baseName[1] != "dat":
            continue
        df, path = readDatFileAndConvertToDataFrame(file_path, baseName[0])
        reducedX, reducedY = reduce_array(df[0], df[1], 0.2)
        xValues.append(reducedX)
        yValues.append(reducedY)

    for i in range(len(xValues)):
        currLabel = 2
        if i < 12:
            currLabel = 2
        elif i < 8:
            currLabel = 1
        elif i < 4:
            currLabel = 0
        else:
            break
        axs[0].plot(
            xValues[i],
            yValues[i],
            label=labels[currLabel],
            linestyle="-",
            color=color_values[i],
        )

    # Add custom legend
    custom_legend = [
        plt.Line2D([0], [0], linestyle="-", color=colors[i], label=legend_labels[i])
        for i in range(len(legend_labels))
    ]

    axs[0].legend(handles=custom_legend)
    axs[0].set_xlabel("Time (s)")
    axs[0].set_ylabel("Cwnd")
    axs[0].set_title("Cwnd of randomly chosen 4 nodes from each set")
    # axs[0].savefig(plot_path + "/cwnd.png")
    # axs[0].close()


# plotting other plots
constants = ["", "router2", "router1"]


dirs = [
    os.path.join(absolute_path, d)
    for d in os.listdir(absolute_path)
    if (
        d != "cwndTraces"
        and d != "plots"
        and os.path.isdir(os.path.join(absolute_path, d))
    )
]

fileNames = ["avgThroughput_0", "avgThroughput_1", "avgThroughput_2"]

xValues = []
yValues = []

for fileName in fileNames:
    basename = fileName
    file_path = os.path.join(dirs[1], fileName)
    # print(basename, basename[0], constants[i])
    df, path = readDatFileAndConvertToDataFrame(file_path, basename)
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
    plot_path + "/avgThroughPut.png",
)


plotCwnds()

plotQueues()

# Adjust layout for better spacing
plt.tight_layout()

# Save the final figure
plt.savefig(plot_path + "/combined_plots.png")
