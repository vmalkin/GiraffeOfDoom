from datetime import datetime, timezone


class Detrender:
    def __init__(self, data):
        self.data = data


def get_delta_p(data, halfwindow):
    nullvalue = np.nan
    returnarray = []
    end_index = len(data) - halfwindow
    # we want to return an array the same size as the input array. We pad the beginning and end with
    # null values. The array is split up thus:
    # [half window at start] <-> [data we work on] <-> [half window at end]
    # IF we were doing a running avg for instance, this would give us a window centred on our chosen data. THis is
    # preferred
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
    print("*** Phase Plots.")
    aggregate_array = data
    plot_utc = []
    plot_seismo = []

    for i in range(1, len(aggregate_array)):
        tim = aggregate_array[i][0]
        tim = datetime.fromtimestamp(tim, tz=timezone.utc)  # datetime object
        siz = aggregate_array[i][1]
        plot_utc.append(tim)
        plot_seismo.append(siz)