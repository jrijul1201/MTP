import os
import pandas as pd
absolute_path = input("Enter the name of the folder: ")

import matplotlib.pyplot as plt

plot_path = absolute_path+ "/plots"

cwnd_folder = absolute_path + "/cwndTraces"

def plotAndSaveGraph(xValue, yValue, title, xLabel, yLabel, filepath):
    fig, ax = plt.subplots()
    ax.plot(xValue, yValue, linestyle='-')
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    ax.set_title(title)
    fig.savefig(filepath)

def readDatFileAndConvertToDataFrame(path, baseName):
    df = pd.read_csv(path, delimiter=' ', header=None)
    return df, plot_path+'/'+baseName+'.png'

for filename in os.listdir(cwnd_folder):
    file_path = os.path.join(cwnd_folder, filename)
    baseName = filename.split('.')
    if(baseName[1] != "dat"):
        continue
    df, path = readDatFileAndConvertToDataFrame(file_path, baseName[0])
    plotAndSaveGraph(df[0], df[1], baseName[0], "Time (s) for the last 25sec", "Cwnd Size", path)

df, path = readDatFileAndConvertToDataFrame(absolute_path+"/queue-size.dat", "queueSize")
plotAndSaveGraph(df[0], df[1], "Queue Size vs time", "Time (s) for the last 25sec", "Queue Size", path)

df, path = readDatFileAndConvertToDataFrame(absolute_path+"/throughput.dat", "throughput")
plotAndSaveGraph(df[0], df[1], "Throughput vs time", "Time (s) for the last 25sec", "Throughput (Mbps)", path)

df, path = readDatFileAndConvertToDataFrame(absolute_path+"/linkUtilization.dat", "linkUtilization")
plotAndSaveGraph(df[0], df[1], "Link Utilization vs time", "Time (s) for the last 25sec", "Link Utilization (%)", path)
