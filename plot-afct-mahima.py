import os
import random
import sys

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# folder_path = "/home/rijul/ns-allinone-3.36.1/ns-3.36.1/examples/results/static-routing-via-virtual/WithThresh/146-TcpNewReno-100"

folder_path = sys.argv[1]
folder_name = sys.argv[2]
plot_path = folder_path + "/plots"

cwnd_folder = folder_path + "/cwndTraces"