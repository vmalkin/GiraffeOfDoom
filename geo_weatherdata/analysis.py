import mgr_database
import standard_stuff
import time
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import matplotlib.dates as mdates
import numpy as np


if __name__ == "__main__":
    end_time = time.time()
    start_time = end_time - 86400
    data = mgr_database.db_data_get(start_time, end_time)
    print(f"Data length: {len(data)}")

    # process data, times for plotting.
    plot_prs = []
    plot_temp = []
    plot_utc = []
    for psx, temp, prs in data:
        plot_prs.append(prs)
        plot_temp.append(temp)
        tim = datetime.fromtimestamp(psx, tz=timezone.utc)  # datetime object
        plot_utc.append(tim)


def plot_singledata(dateformatstring, dateobjects, singledataarray, tickinterval, plotcolour, plottitle, savefile):
    fig, ax = plt.subplots(layout="constrained", figsize=(8, 8), dpi=140)
