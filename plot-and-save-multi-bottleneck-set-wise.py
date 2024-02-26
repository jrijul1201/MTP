import os
import matplotlib.pyplot as plt


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


def read_all_fct_dat_files(folder_path):
    all_data = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == "fct.dat":
                file_path = os.path.join(root, file)
                folder_name = os.path.basename(os.path.dirname(file_path))
                folder_name = folder_name.replace("afct-", "afct2084-")
                folder_name = folder_name.replace("afct", "qth")
                all_data[folder_name] = read_fct_dat_file(file_path)
    return sort_dict(all_data)


def plot_fct_stats(set_data, stat_name, save_path=None):
    plt.figure()
    for set_name, stats in set_data.items():
        plt.plot(stats.keys(), stats.values(), label=f"Set {set_name}")
    plt.xlabel("Folder Name")
    plt.ylabel(stat_name)
    plt.title(f"{stat_name} Across Sets")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()  # Adjust layout to prevent label cutoff

    if save_path:
        plt.savefig(os.path.join(save_path, f"{stat_name}_across_sets.png"))
    # plt.show()


def calculate_set_stats(sets, all_data):
    set_stats = {"Average FCT": {}, "Minimum FCT": {}, "Maximum FCT": {}}
    for set_range in sets:
        set_name = f"{set_range[0]}-{set_range[1]}"
        averages = {}
        minimums = {}
        maximums = {}
        for folder_name, folder_data in all_data.items():
            folder_values = [
                folder_data[i] for i in range(set_range[0], set_range[1] + 1)
            ]
            averages[folder_name] = sum(folder_values) / len(folder_values)
            minimums[folder_name] = min(folder_values)
            maximums[folder_name] = max(folder_values)
        set_stats["Average FCT"][set_name] = averages
        set_stats["Minimum FCT"][set_name] = minimums
        set_stats["Maximum FCT"][set_name] = maximums
    return set_stats


if __name__ == "__main__":
    folder_path = (
        "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/multi-bottleneck"
    )
    save_path = folder_path
    all_data = read_all_fct_dat_files(folder_path)
    sets = [(0, 4), (5, 9), (10, 23), (24, 28), (29, 31), (32, 52), (53, 56), (57, 59)]
    set_stats = calculate_set_stats(sets, all_data)

    for stat_name, stats_data in set_stats.items():
        plot_fct_stats(stats_data, stat_name, save_path)
