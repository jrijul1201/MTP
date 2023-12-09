import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

# Your data
parking_dataset = [
    # [
    #     {
    #         "label": "60-TcpCubic-10/A",
    #         "withoutThresh": 1.7320508075688772,
    #         "withThresh": 5.5420607263529345,
    #     },
    #     {
    #         "label": "60-TcpCubic-10/B",
    #         "withoutThresh": 1.4142135623730951,
    #         "withThresh": 3.3166247903554,
    #     },
    #     {
    #         "label": "60-TcpCubic-10/C",
    #         "withoutThresh": 1.7320508075688772,
    #         "withThresh": 4.242640687119285,
    #     },
    # ],
    # [
    #     {
    #         "label": "60-TcpCubic-200/A",
    #         "withoutThresh": 1.7320508075688772,
    #         "withThresh": 2.449489742783178,
    #     },
    #     {
    #         "label": "60-TcpCubic-200/B",
    #         "withoutThresh": 1.7320508075688772,
    #         "withThresh": 1.0,
    #     },
    #     {
    #         "label": "60-TcpCubic-200/C",
    #         "withoutThresh": 1.7320508075688772,
    #         "withThresh": 2.23606797749979,
    #     },
    # ],
    [
        {
            "label": "60-TcpNewReno-10/A",
            "withoutThresh": 5.4845236803208355,
            "withThresh": 5.506757444354039,
        },
        {
            "label": "60-TcpNewReno-10/B",
            "withoutThresh": 5.65194165260439,
            "withThresh": 5.529537201352217,
        },
        {
            "label": "60-TcpNewReno-10/C",
            "withoutThresh": 5.517648452415616,
            "withThresh": 5.52896481085787,
        },
    ],
    [
        {
            "label": "60-TcpNewReno-200/A",
            "withoutThresh": 5.431390245600108,
            "withThresh": 5.50943687032524,
        },
        {
            "label": "60-TcpNewReno-200/B",
            "withoutThresh": 5.385164807134504,
            "withThresh": 5.500959512262888,
        },
        {
            "label": "60-TcpNewReno-200/C",
            "withoutThresh": 5.497474167490214,
            "withThresh": 5.518604896167147,
        },
    ],
]


single_dataset = [
    [
        {
            "label": "60-TcpNewReno-200",
            "withoutThresh": 7.814516406449389,
            "withThresh": 7.750124322278954,
        },
    ],
    [
        {
            "label": "60-TcpNewReno-10",
            "withoutThresh": 7.920788793225003,
            "withThresh": 7.817058421198173,
        },
    ]
    # {
    #     "label": "60-TcpCubic-200",
    #     "withoutThresh": 2.0,
    #     "withThresh": 2.6457513110645907,
    # },
    # {
    #     "label": "60-TcpCubic-10",
    #     "withoutThresh": 1.7320508075688772,
    #     "withThresh": 7.836939667042808,
    # },
]

corr_single_dataset = [
    [
        {
            "label": "60-TcpNewReno-200",
            "withoutThresh": 0.1951,
            "withThresh": 0.0166,
        },
    ],
    [
        {
            "label": "60-TcpNewReno-10",
            "withoutThresh": 0.2392,
            "withThresh": 0.019,
        },
    ],
]

corr_parking_dataset = [
    [
        {
            "label": "60-TcpNewReno-200",
            "withoutThresh": 0.1097,
            "withThresh": 0.0373,
        },
    ],
    [
        {
            "label": "60-TcpNewReno-10",
            "withoutThresh": 0.0752,
            "withThresh": 0.0249,
        },
    ],
]


def frob_plot(data, name, xaxis, yaxis):
    for entry in data:
        label = entry["label"]
        without_thresh_norm = entry["withoutThresh"]
        with_thresh_norm = entry["withThresh"]

        # Plotting the bars
        plt.bar(
            [f"F-{label}", f"T-{label}"],
            [without_thresh_norm, with_thresh_norm],
            color=["skyblue", "pink"],
        )

    plt.xticks(rotation=25, ha="right")
    plt.title(yaxis + " vs " + xaxis)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    # Creating custom handles for the legend
    without_thresh_patch = mpatches.Patch(
        color="skyblue", label="Without Threshold AQM"
    )
    with_thresh_patch = mpatches.Patch(color="pink", label="With Threshold AQM")

    # Adding legend with custom handles
    plt.legend(handles=[without_thresh_patch, with_thresh_patch], loc="upper right")
    plt.tight_layout()

    plt.savefig(name + ".png")
    plt.close()


# for data in parking_dataset:
#     frob_plot(data, "parking-lot-" + data[0]["label"].split("/")[0], "Set", "Synchronization Loss")

# for data in single_dataset:
#     frob_plot(
#         data, "single-bottleneck-" + data[0]["label"].split("/")[0], "Configuration", "Synchronization Loss"
#     )

for data in corr_parking_dataset:
    frob_plot(
        data,
        "corr-parking-lot-" + data[0]["label"].split("/")[0],
        "Configuration",
        "Congestion Window Correlation",
    )

for data in corr_single_dataset:
    frob_plot(
        data,
        "corr-single-bottleneck-" + data[0]["label"].split("/")[0],
        "Configuration",
        "Congestion Window Correlation",
    )
