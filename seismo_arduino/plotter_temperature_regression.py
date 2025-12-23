from datetime import timezone, datetime
import constants as k
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator
import os
import class_aggregator
from scipy.signal import spectrogram, detrend
from datetime import timedelta
import numpy as np


def wrapper(data):
    #  filtering improved with ChatGPT
    #  tilt(t)=a⋅T(t)+b+residual(t)
    # T = temperature at time (t)
    # decimate data for this. 5 minute intervals
    window = 10 * 60 * 5
    aggregate_array = class_aggregator.aggregate_data(window, data)
    aggregate_array.pop(0)

    plot_utc = []
    plot_seismo = []
    plot_temp = []
    plot_press = []

    for i in range(1, len(aggregate_array)):
        tim = aggregate_array[i].get_avg_posix()
        tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
        siz = aggregate_array[i].get_data_avg(aggregate_array[i].data_seismo)
        tmp = aggregate_array[i].get_data_avg(aggregate_array[i].data_temperature)
        prs = aggregate_array[i].get_data_avg(aggregate_array[i].data_pressure)

        plot_utc.append(tim)
        plot_seismo.append(siz)
        plot_temp.append(tmp)
        plot_press.append(prs)



