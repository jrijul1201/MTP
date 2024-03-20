import os
import matplotlib.pyplot as plt
import sys
import statistics


FCT_PATH = "/TcpLinuxReno/fct.dat"

filePath = sys.argv[1]

QTH_AQM = {2084: "Droptail", 15: "Threshold15", 100: "Threshold100"}


def read_fct_dat_file(file_path):
    data = {}
    with open(file_path, "r") as file:
        next(file)  # Skip header
        for line in file:
            flow, fct = line.strip().split("\t")
            data[int(flow)] = float(fct)
    return data


def sort_dict(myDict):
    myKeys = list(myDict.keys())
    myKeys.sort()
    return {i: myDict[i] for i in myKeys}


def calculate_set_stats(sets, folder_data):
    set_stats = {}
    for set_range in sets:
        set_name = f"{set_range[0]}-{set_range[1]}"
        set_stats[set_name] = {}
        folder_values = [folder_data[i] for i in range(set_range[0], set_range[1] + 1)]
        average = sum(folder_values) / len(folder_values)
        minimum = min(folder_values)
        maximum = max(folder_values)
        stddev = statistics.stdev(folder_values)
        set_stats[set_name]["average"] = round(average, 2)
        set_stats[set_name]["minimum"] = round(minimum, 2)
        set_stats[set_name]["maximum"] = round(maximum, 2)
        set_stats[set_name]["stddev"] = round(stddev, 2)
    return set_stats


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python script.py input_file output_file folder_name")
        sys.exit(1)
    folder_path = sys.argv[1]
    save_path = "/home/dipesh/Desktop/ns-allinone-3.36.1/ns-3.36.1/examples/results/processed-data/"
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    fct_data = read_fct_dat_file(folder_path + FCT_PATH)
    sets = [(0, 4), (5, 9), (10, 23), (24, 28), (29, 31), (32, 52), (53, 56), (57, 59)]
    set_stats = calculate_set_stats(sets, fct_data)
    folder_name = os.path.basename(folder_path)
    folder_name = folder_name.replace("afct-", "afct2084-")
    folder_name = folder_name.replace("afct", "")
    qth, rtt = folder_name.split("-")
    rtt = rtt[:-2]
    for setName, setData in set_stats.items():
        fileName = f"{QTH_AQM[int(qth)]}-{setName}.txt"
        path_to_append = save_path + fileName
        if not os.path.exists(path_to_append):
            with open(path_to_append, "w") as file:
                file.write(f"rtt\tavg\tmin\tmax\tstddev" + "\n")

        with open(path_to_append, "a") as file:
            avg = setData["average"]
            mini = setData["minimum"]
            maxi = setData["maximum"]
            stddevi = setData["stddev"]
            file.write(f"{rtt}\t{avg}\t{mini}\t{maxi}\t{stddevi}" + "\n")
