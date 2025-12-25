from datetime import datetime, timezone

import numpy as np


def get_delta_p(data, halfwindow):
    nullvalue = np.nan
    returnarray = []
    end_index = len(data) - halfwindow

    if len(data) > halfwindow:
        for i in range(0, len(data)):
            if halfwindow < i < end_index:
                window_data = data[i - halfwindow: i + halfwindow]
                # j = window_data[-1] - window_data[0]
                j = np.nanmax(window_data) - np.nanmin(window_data)
                j = round(j, 3)
                returnarray.append(j)
            else:
                returnarray.append(nullvalue)
    else:
        for _ in data:
            returnarray.append(nullvalue)
    return returnarray


def wrapper(data):
    print("*** Detrending.")
    aggregate_array = data
    data_utc = []
    data_seismo = []

    for i in range(1, len(aggregate_array)):
        tim = aggregate_array[i][0]
        tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
        siz = aggregate_array[i][1]
        data_utc.append(tim)
        data_seismo.append(siz)

    plot_utc = []
    plot_seismo = []
    readings_per_sec = 10
    detrend_half_window = readings_per_sec * 60 * 5
    end_index = len(data_seismo) - detrend_half_window

    for i in range(0, len(data_seismo)):
        if detrend_half_window < i < end_index:
            window_data = data_seismo[i - detrend_half_window: i + detrend_half_window]
            dd = data_seismo[i] - np.nanmean(window_data)
            dt = data_utc[i]
            plot_seismo.append(dd)
            plot_utc.append(dt)
            if i % 100 == 0:
                print(f'{i} / {len(data_seismo)}')




