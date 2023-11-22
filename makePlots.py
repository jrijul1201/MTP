import os
import pandas as pd
import random
import matplotlib.pyplot as plt
absolute_path = input("Enter the name of the folder: ")

labels = ["A","B","C"]

queueSizes = ["queue1", "queue2"]
plot_path = absolute_path+ "/plots"

cwnd_folder = absolute_path + "/cwndTraces"
colors = ["#CC0000", '#0066CC', "#339933"]

def reduce_array(arr, arrX, target_difference):
    reduced_array = [arr[0]]  # Start with the first element
    reduced_x = [arrX[0]]

    for i in range(1, len(arr)):
        if arr[i] - reduced_array[-1] >= target_difference:
            reduced_array.append(arr[i])
            reduced_x.append(arrX[i])

    return reduced_array, reduced_x



def plotAndSaveGraph(xValues, yValues, label, title, xLabel, yLabel, filepath):
    for i in range(len(xValues)):
        plt.plot(xValues[i], yValues[i], label = label[i])
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.legend()
    plt.savefig(filepath)
    plt.close()

def readDatFileAndConvertToDataFrame(path, baseName):
    df = pd.read_csv(path, delimiter=' ', header=None)
    return df, plot_path+'/'+baseName+'.png'

# plot cwnd traces

xValues = []
yValues = []

routerPaths = [absolute_path+"/router0/queueSize.dat", absolute_path+"/router1/queueSize.dat"]

def plotQueues():
    xValues = []
    yValues = []
    for queueSizePath in routerPaths:
        df, path = readDatFileAndConvertToDataFrame(queueSizePath, "")
        reducexX, reducedY = reduce_array(df[0], df[1], 0.2)
        xValues.append(reducexX)
        yValues.append(reducedY)
    plotAndSaveGraph(xValues, yValues, queueSizes, "Queue size vs Time(s)", "Time (s)", "Queue size", plot_path+"/queueSize.png" )



def plotCwnds():
    dirList = os.listdir(cwnd_folder)

    length = len(dirList)
    random_integers = [ i+j for i in range(0,3) for j in random.sample(range(0,  length-1), 4)]

    # Divide the array into three parts
    for i in random_integers:
        filename = dirList[i]
        file_path = os.path.join(cwnd_folder, filename)
        baseName = filename.split('.')
        if(baseName[1] != "dat"):
            continue
        df, path = readDatFileAndConvertToDataFrame(file_path, baseName[0])
        reducedX, reducedY = reduce_array(df[0], df[1], 0.2)
        xValues.append(reducedX)
        yValues.append(reducedY)

    for i in range(len(xValues)):
        currLabel = 2
        if(i<12):
            currLabel = 2
        if(i<8):
            currLabel = 1
        if(i<4):
            currLabel = 0
        plt.plot(xValues[i], yValues[i], label = labels[currLabel], linestyle='-', color = colors[currLabel])
    plt.xlabel("Time (s)")
    plt.ylabel("Cwnd")
    plt.title("Cwnd of randomly chosen 4 nodes from each set")
    plt.savefig(plot_path+'/cwnd.png')
    plt.close()

# plotting other plots
constants = ["", "router2", "router1"]


dirs = [os.path.join(absolute_path, d) for d in os.listdir(absolute_path) if (d!="cwndTraces" and d!= "plots" and os.path.isdir(os.path.join(absolute_path, d)))]

fileNames = ["avgThroughput_0", "avgThroughput_1", "avgThroughput_2"]

xValues = []
yValues = []

for fileName in fileNames:
    basename = fileName
    file_path = os.path.join(dirs[0], fileName)
    # print(basename, basename[0], constants[i])
    df, path = readDatFileAndConvertToDataFrame(file_path, basename)
    reduxedX, reducedY = reduce_array(df[0], df[1], 0.2)
    xValues.append(reduxedX)
    yValues.append(reducedY)

plotAndSaveGraph(xValues, yValues, labels,"Average throughput vs Time", "Time (s)", "Avg Throughput", plot_path+"/avgThroughPut.png")



plotCwnds()

plotQueues()









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