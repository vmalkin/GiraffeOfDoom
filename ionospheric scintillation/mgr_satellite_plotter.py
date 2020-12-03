from matplotlib import pyplot as plt
from matplotlib import ticker as ticker
from datetime import datetime
from time import time
from numpy import nan
import os


timeformat = '%d %H:%M'
dateformat = '%Y-%m-%d'
working_dir = "images"
epoch_now = int(time())
epoch_start = int(epoch_now - 86400)
binsize = 60

class GPSSatellite:
    def __init__(self, sat_name):
        self.name = sat_name
        self.available = False
        self.satdata = self.init_satdata()

    def init_satdata(self):
        returnarray = []
        dt = epoch_start
        for i in range(0, 1442):
            # array is date, alt, snr, s4
            returnarray.append([posix2utc(dt), nan, nan, nan])
            # returnarray.append([posix2utc(dt), "", "", ""])
            dt = dt + binsize
        return returnarray


def create_satellite_list(constellationname):
    returnlist = []
    for i in range(0, 300):
        name = constellationname + str(i)
        gps = GPSSatellite(name)
        returnlist.append(gps)
    return returnlist


def create_chart(sat):
    try:
        name = sat.name + ".jpg"
        x = []
        y1 = []
        y2 = []
        y3 = []
        for data in sat.satdata:
            x.append(data[0])
            y1.append(data[1])
            y2.append(data[2])
            y3.append(data[3])

        s4, ax = plt.subplots(figsize=[6,3], dpi=100)
        tic_space = 30
        ax.xaxis.set_major_locator(ticker.MultipleLocator(tic_space))
        ax.tick_params(axis='x', labelrotation=45)
        ax.set_ylim(0, 100)
        ax.set_xlabel("Time UTC")
        ax.set_ylabel("Altitude, S/N, S4 (deg, dB, %)")
        plt.plot(x, y1, color="red")
        plt.plot(x, y2, color="blue")
        plt.plot(x, y3, color="black")
        plt.rcParams.update({'font.size': 6})
        filepath = working_dir + "//" + name
        s4.tight_layout()
        plt.savefig(filepath)
    except:
        print("Unable to save image file")
    plt.close('all')


def posix2utc(posixtime):
    # print(posixtime)
    # utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    utctime = datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime

def get_index(currentposix):
    indexvalue = (currentposix - epoch_start) / binsize
    indexvalue = int(round(indexvalue,0))
    return indexvalue

def create_directory(directory):
    try:
        os.makedirs(directory)
        print("Logfile directory created.")
    except:
        if not os.path.isdir(directory):
            print("Unable to create log directory")

# Wrapper
def create_individual_plots(resultlist):
    if os.path.isdir(working_dir) is False:
        print("Creating log file directory...")
        create_directory(working_dir)

    GPGSV = create_satellite_list("gps_")
    GLGSV = create_satellite_list("glonass_")

    #  Resultlist should have the format
    # sat_id, posixtime, alt, az, s4, snr
    for sat in resultlist:
        detail = sat[0].split("_")
        name = detail[0]
        number = int(detail[1])
        if name == "gps":
            # dp = (sat[0], posix2utc(sat[1]), sat[2], sat[3], sat[4], sat[5])
            index = get_index(sat[1])
            GPGSV[number].available = True
            GPGSV[number].satdata[index][1] = sat[2]
            GPGSV[number].satdata[index][2] = sat[4]
            GPGSV[number].satdata[index][3] = sat[5]

        if name == "glonass":
            # dp = (sat[0], posix2utc(sat[1]), sat[2], sat[3], sat[4], sat[5])
            index = get_index(sat[1])
            GPGSV[number].available = True
            GPGSV[number].satdata[index][1] = sat[2]
            GPGSV[number].satdata[index][2] = sat[4]
            GPGSV[number].satdata[index][3] = sat[5]

    for sat in GPGSV:
        if sat.available == True:
            create_chart(sat)

    for sat in GLGSV:
        if sat.available == True:
            create_chart(sat)
