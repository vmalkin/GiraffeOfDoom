"""
Generic parser for Spectrum Lab save files.
Customised for Wideband Magnetic Riometer

Data file lines have the format of:
UTCdatetime, data_a, data_b, data_c, etc...
"""
import time
from statistics import median, mean
from datetime import datetime
from calendar import timegm
import numpy as np
import re
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# datafile = "c://temp//hiss.csv"
# datafile = "c://temp//harmonics.csv"
datafile = "hiss.csv"
regex = r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d"
dt_format = "%Y-%m-%d %H:%M:%S"
stationname = "dna_hiss"
graphing_file = stationname + "_graph.csv"
median_window = 2  # Full window = halfwindow * 2 + 1
average_window = 90

def filter_average(list):
    returnlist = []
    for i in range(average_window, len(list) - average_window):
        templist = []
        for j in range(-1 * average_window, average_window):
            data = float(list[i+j])
            templist.append(data)
        avg_data = mean(templist)
        avg_data = round(avg_data, 3)
        returnlist.append(avg_data)
    return returnlist


def filter_median(item_list):
    """
    Takes in a list of DataPoints and performs a median filter on the list. The list is truncated at the start
    and end by one halfwindow
    """
    returnlist = []

    for i in range(median_window, len(item_list) - median_window):
        data_store = []
        for j in range(0 - median_window, median_window + 1):
            d = float(item_list[i + j])
            data_store.append(d)
        medianvalue = median(data_store)
        returnlist.append(medianvalue)
    return returnlist


def utc_to_posix(utc_time):
    date_obj = datetime.strptime(utc_time, dt_format)
    posixtime = timegm(date_obj.timetuple())
    return posixtime


def open_file(datafile):
    returnlist = []
    with open(datafile, "r") as c:
        for line in c:
            line = line.strip("\n")
            line = line.split(",")
            datething = line[0]
            if re.match(regex, datething):
                returnlist.append(line)
    return returnlist


def get_header(datafile):
    with open(datafile, "r") as c:
        for line in c:
            line = line.strip()
            header = line
            break
    return header

def parse_file(list):
    starttime = time.time() - 86400
    returnlist = []
    for line in list:
        # line = line.strip("\n")
        # line = line.split(",")
        datething = line[0]
        if re.match(regex, datething):
            if utc_to_posix(datething) > starttime:
                returnlist.append(line)
    return returnlist


def filter_nulls(data):
    null = None
    returnlist = []
    for item in data:
        if item == 0:
            returnlist.append(null)
        elif item > 500:
            returnlist.append(null)
        else:
            returnlist.append(item)
    return returnlist


def plot_graph(datelabels, headings, data):
    savefile = "hiss.jpg"
    width = 1500
    height = 640
    # fig = go.Figure()
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    for i in range(0, len(data)):
        print(headings[i])
        fig.add_trace(go.Scatter(x=datelabels, y=data[i], mode="lines", name=headings[i]), secondary_y=True)

    fig.update_layout(width=width, height=height, title="Hiss",
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>",
                      yaxis_title="CME Coverage")
    fig.update_layout(plot_bgcolor="#a0a0a0", paper_bgcolor="#a0a0a0")

    fig.write_image(file=savefile, format='jpg')



if __name__ == "__main__":
    datalist = open_file(datafile)
    # header = get_header(datafile)
    data_last_24_hours = parse_file(datalist)
    npdata = np.array(data_last_24_hours)
    rowlen = npdata.shape[1]

    # Slice the array into separate lists for each column
    master_data = []
    datetimes = npdata[:, 0]
    for i in range(1, rowlen):
        master_data.append(npdata[:, i])

    # Perform whatever functions to the lists
    filtered = []
    for data in master_data:
        d = filter_median(data)
        d = filter_average(d)
        filtered.append(d)

    # FINALLY Remove extreme values and replace with a null
    nulled = []
    for data in filtered:
        nulled.append(filter_nulls(data))

    # # Reconstitute the lists into a single file for display
    # # AFter the filtering processes, the length of data will differ from the original
    # # data. Start iterating from the correct record in datetime to compensate
    # difference = len(datetimes) - len(nulled[0])
    # startindex = int(difference / 2)
    # with open(graphing_file, "w") as g:
    #     g.write(header + "\n")
    #     for i in range(startindex, len(datetimes) - startindex - 1):
    #         dp = datetimes[i] + ","
    #         for data in nulled:
    #             dp = dp + str(data[i - startindex]) + ","
    #         dp = dp[:-1]
    #         g.write(dp + "\n")
    # g.close()

    difference = len(datetimes) - len(nulled[0])
    startindex = int(difference / 2)
    newdates = []
    for i in range(startindex, len(datetimes) - startindex - 1):
        newdates.append(datetimes[i])

    # CReate a graph in plotly
    labels = ["22Hz", "120Hz", "14kHz"]
    plot_graph(newdates, labels, nulled)
