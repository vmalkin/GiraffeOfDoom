from matplotlib import pyplot as plt
from matplotlib import ticker as ticker
from datetime import datetime
from time import time

utc_format = '%d %H:%M'
working_dir = "images"


def posix2utc(posixtime):
    utctime = datetime.utcfromtimestamp(int(posixtime)).strftime(utc_format)
    return utctime


def create_scatterplot_chart(xdata, ydata):
    name = "snr.png"
    filepath = working_dir + "//" + name
    snr, ax = plt.subplots(figsize=[24,7], dpi=100)
    tic_major = 60
    tic_minor = 10
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tic_major))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(tic_minor))
    ax.grid(True, which='major', color="#ccb3b3")
    ax.grid(True, which='minor', color="#e0e0e0")
    ax.tick_params(axis='x', labelrotation=90)
    plt.scatter(xdata, ydata, marker="o", s=1, alpha=0.9, color='#000000')
    # plt.show()
    plt.savefig(filepath)
    plt.close('all')


def create_list(queryresults, indexpos):
    returnlist = []
    for line in queryresults:
        if line[2] > 20:
            d = line[indexpos]
            returnlist.append(d)
    return returnlist


# query results format:
# sat_id, posixtime, alt, az, s4, snr
def convert_time(times):
    returnlist = []
    for item in times:
        t = posix2utc(item)
        returnlist.append(t)
    return returnlist


def wrapper(queryresults):
    xdata = create_list(queryresults, 1)
    xdata = convert_time(xdata)
    ydata = create_list(queryresults, 5)

    create_scatterplot_chart(xdata, ydata)