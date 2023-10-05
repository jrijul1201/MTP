import os
import pandas as pd
folder_name = input("Enter the name of the folder: ")

import matplotlib.pyplot as plt
    
absolute_path = "/home/dipesh/ns-allinone-3.36.1/ns-3.36.1/" + folder_name

plot_path = absolute_path+ "/plots"

cwnd_folder = absolute_path + "/cwndTraces"

os.mkdir(plot_path)

def plotAndSaveGraph(xValue, yValue, title, xLabel, yLabel, filepath):
    plt.plot(xValue, yValue, linestyle='-')
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.savefig(filepath)
    plt.show()

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
