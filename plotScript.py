import os
import pandas as pd
import random
absolute_path = input("Enter the name of the folder: ")

import matplotlib.pyplot as plt

plot_path = absolute_path+ "/plots"

cwnd_folder = absolute_path + "/cwndTraces"

def plotAndSaveGraph(xValues, yValues, title, xLabel, yLabel, filepath):
    fig, ax = plt.subplots()
    for i in range(len(xValues)):
        ax.plot(xValues[i], yValues[i], linestyle='-')
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    ax.set_title(title)
    fig.savefig(filepath)

def readDatFileAndConvertToDataFrame(path, baseName):
    df = pd.read_csv(path, delimiter=' ', header=None)
    return df, plot_path+'/'+baseName+'.png'

# plot cwnd traces

xValues = []
yValues = []

dirList = os.listdir(cwnd_folder)

random_integers = random.sample(range(0,  dirList.__len__()), 8)

for i in random_integers:
    filename = dirList[i]
    file_path = os.path.join(cwnd_folder, filename)
    baseName = filename.split('.')
    if(baseName[1] != "dat"):
        continue
    df, path = readDatFileAndConvertToDataFrame(file_path, baseName[0])
    xValues.append(df[0])
    yValues.append(df[1])

plotAndSaveGraph(xValues, yValues, "Cwnd of randomly chosen 8 nodes", "Time (s) for the last 25sec", "Cwnd Size", plot_path+'/cwnd.png')

# plotting other plots
constants = ["", "router2", "router1"]
# listing all req directories
dirs = [os.path.join(absolute_path, d) for d in os.listdir(absolute_path) if (d!="cwndTraces" and d!= "plots" and os.path.isdir(os.path.join(absolute_path, d)))]

# print(dirs)

for i in range(1,3):
    for fileName in os.listdir(dirs[i]):
        basename = fileName.split('.')
        file_path = os.path.join(dirs[i], fileName)
        if(basename[1] != "dat" or basename[0] == "drop"):
            continue
        # print(basename, basename[0], constants[i])
        df, path = readDatFileAndConvertToDataFrame(file_path, basename[0]+constants[i])
        plotAndSaveGraph([df[0]], [df[1]], basename[0] + " vs time", "Time (s) for the last 25sec", basename[0]+constants[i], path)
        plt.close()

throughput = os.listdir(dirs[0])

fileNames = ["avgThroughput_0", "avgThroughput_1", "avgThroughput_2"]

for fileName in fileNames:
    basename = fileName
    file_path = os.path.join(dirs[0], fileName)
    # print(basename, basename[0], constants[i])
    df, path = readDatFileAndConvertToDataFrame(file_path, basename)
    plotAndSaveGraph([df[0]], [df[1]], basename + " vs time", "Time (s) for the last 25sec", basename, path)
    plt.close()
















































# df, path = readDatFileAndConvertToDataFrame(absolute_path+"/throughput.dat", "throughput")
# plotAndSaveGraph([df[0]], [df[1]], "Throughput vs time", "Time (s) for the last 25sec", "Throughput (Mbps)", path)

# df, path = readDatFileAndConvertToDataFrame(absolute_path+"/linkUtilization.dat", "linkUtilization")
# plotAndSaveGraph([df[0]], [df[1]], "Link Utilization vs time", "Time (s) for the last 25sec", "Link Utilization (%)", path)

# xValues = []
# yValues = []

# dirList = os.listdir(cwnd_folder)

# random_integers = random.sample(range(0,  dirList.__len__()), 8)
# # print (random_integers, dirList, dirList.__len__())

# for i in random_integers:
#     filename = dirList[i]
#     file_path = os.path.join(cwnd_folder, filename)
#     baseName = filename.split('.')
#     if(baseName[1] != "dat"):
#         continue
#     df, path = readDatFileAndConvertToDataFrame(file_path, baseName[0])
#     xValues.append(df[0])
#     yValues.append(df[1])

# plotAndSaveGraph(xValues, yValues, "Cwnd of randomly chosen 8 nodes", "Time (s) for the last 25sec", "Cwnd Size", plot_path+'/cwnd.png')