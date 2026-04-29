import mgr_database
import standard_stuff
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np


if __name__ == "__main__":
    end_time = time.time()
    # print("Start time:", standard_stuff.posix2utc(1777442234.41846, timeformat='%Y-%m-%d %H:%M:%S'))
    start_time = end_time - 86400

    data = mgr_database.db_data_get(start_time, end_time)
    print(f"Data length: {len(data)}")
    for psx, temp, prs in data:
        print(f"{standard_stuff.posix2utc(psx, timeformat='%Y-%m-%d %H:%M:%S')},{temp},{prs}")
        # print(f"{psx},{temp},{prs}")


def plot_multi(dateformatstring, dateobjects, singledataarray, tickinterval, plotcolour, plottitle, savefile):
    pass