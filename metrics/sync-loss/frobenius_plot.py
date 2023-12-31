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

new_single_dataset = [
    [
        {
            "label": "60-TcpCubic-200",
            "withoutThresh": 8.913489255158508,
            "withThresh": 8.555750713243123,
        }
    ],
    [
        {
            "label": "60-TcpCubic-10",
            "withoutThresh": 8.454103692423834,
            "withThresh": 7.981505163102372,
        }
    ],
    [
        {
            "label": "60-TcpNewReno-200",
            "withoutThresh": 8.391237798551034,
            "withThresh": 8.719945060204743,
        }
    ],
    [
        {
            "label": "60-TcpNewReno-10",
            "withoutThresh": 8.4058924937424,
            "withThresh": 8.171925918042874,
        }
    ],
]

new_parking_dataset = [
    [
        {
            "label": "60-TcpCubic-10/A",
            "withoutThresh": 5.835610482367378,
            "withThresh": 5.598339116841516,
        },
        {
            "label": "60-TcpCubic-10/B",
            "withoutThresh": 6.524617121270629,
            "withThresh": 5.966852257286757,
        },
        {
            "label": "60-TcpCubic-10/C",
            "withoutThresh": 10.469185992280844,
            "withThresh": 5.658801987695796,
        },
    ],
    [
        {
            "label": "60-TcpCubic-200/A",
            "withoutThresh": 5.910110231729086,
            "withThresh": 5.686464016932932,
        },
        {
            "label": "60-TcpCubic-200/B",
            "withoutThresh": 4.7807021846884385,
            "withThresh": 5.3584453443080395,
        },
        {
            "label": "60-TcpCubic-200/C",
            "withoutThresh": 6.024499321164452,
            "withThresh": 6.110895445032672,
        },
    ],
    [
        {
            "label": "60-TcpNewReno-10/A",
            "withoutThresh": 5.93253739979783,
            "withThresh": 5.596800512104149,
        },
        {
            "label": "60-TcpNewReno-10/B",
            "withoutThresh": 5.76204589009027,
            "withThresh": 5.6533659702287675,
        },
        {
            "label": "60-TcpNewReno-10/C",
            "withoutThresh": 4.684786251497737,
            "withThresh": 5.626084832360204,
        },
    ],
    [
        {
            "label": "60-TcpNewReno-200/A",
            "withoutThresh": 5.678259450349863,
            "withThresh": 5.8632376426248305,
        },
        {
            "label": "60-TcpNewReno-200/B",
            "withoutThresh": 4.8125094195835345,
            "withThresh": 6.243972629063312,
        },
        {
            "label": "60-TcpNewReno-200/C",
            "withoutThresh": 3.986086914367133,
            "withThresh": 6.450517472823864,
        },
    ],
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


for data in new_parking_dataset:
    frob_plot(
        data,
        "parking-lot-" + data[0]["label"].split("/")[0],
        "Set",
        "Synchronization Loss",
    )

for data in new_single_dataset:
    frob_plot(
        data,
        "single-bottleneck-" + data[0]["label"].split("/")[0],
        "Configuration",
        "Synchronization Loss",
    )

# for data in corr_parking_dataset:
#     frob_plot(
#         data,
#         "corr-parking-lot-" + data[0]["label"].split("/")[0],
#         "Configuration",
#         "Congestion Window Correlation",
#     )

# for data in corr_single_dataset:
#     frob_plot(
#         data,
#         "corr-single-bottleneck-" + data[0]["label"].split("/")[0],
#         "Configuration",
#         "Congestion Window Correlation",
#     )
