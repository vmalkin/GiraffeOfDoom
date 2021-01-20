# Create individual plots for each GPS satellite showing altitude, SNR, S4
import datetime
import plotly.graph_objects as go
import constants as k
from numpy import NaN
import time

# The max constellation ID number we could expect a satellite to report.
constellation_id_max_value = 200


class Satellite:
    def __init__(self, tstart, tnow):
        self._timestart = tstart
        self._timenow = tnow
        self.name = ""
        self.data = self.create_datastore()
        # to be used when parsing the list for sats that have been updated, speed things up
        self.update_flag = False

    def create_datastore(self):
        """Create a datastore to hold readings for each minute"""
        # _steps = int((self._timenow - self._timestart) / 60)
        _steps = 1450
        d = []
        for i in range(0, _steps):
            d.append(NaN)
        return d

    def time_index(self, timevalue):
        """Using the timevalue, create an index value to drop data into it's correct slot in the datastore"""
        t = timevalue - self._timestart
        t = int(round((t / 60), 0))
        return t

    def update_data(self, datavalue, timestamp):
        self.data[self.time_index(timestamp)] = datavalue


def posix2utc(posixtime):
    timeformat = '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def create_satellite_dictionary():
    """
    Creates a lookup table so when we supply the satellite name and number, we get a unique index value.
    THis allows us to go thru the scrambled list of satellites in a single pass
    """
    s = {}
    constellation = "GPGSV_"
    for i in range(0, constellation_id_max_value + 1):
        key = constellation + str(i)
        value = i
        s[key] = value

    constellation = "GLGSV_"
    for i in range(1, constellation_id_max_value + 1):
        j = constellation_id_max_value + i
        key = constellation + str(i)
        value = j  # continuing the index from the end of i
        s[key] = value
    return s


def create_constellation(starttime, nowtime):
    c = []
    for i in range(0, (constellation_id_max_value * 2 + 10)):
        s = Satellite(starttime, nowtime)
        c.append(s)
    return c


def plot(satlist, tlabels):
    for satellite in satlist:
        xval = tlabels
        yval = satellite.data
        name = satellite.name
        savefile = k.imagesdir + "//" + satellite.name + ".jpg"
        plot_title = "S4 Index SatID: " + name

        data = go.Scatter(x=xval, y = yval, mode="lines")
        fig = go.Figure(data)
        fig.update_yaxes(range=[1, 100], gridcolor='#505050')
        fig.update_xaxes(nticks=24, tickangle=45, gridcolor='#505050')
        fig.update_layout(width=800, height=600, title=plot_title, xaxis_title="Date/time UTC", yaxis_title="S4 Index", plot_bgcolor="#101010")
        fig.update_traces(line=dict(width=2, color="rgba(0,255,255,0.5)"))
        fig.write_image(file=savefile, format='jpg')


# query format:
# ('satID', posixtime, alt, az, s4, snr)
# Query is sorted in posixtime order.
def wrapper(query):
    time_now = int(time.time())
    time_start = time_now - (60 * 60 * 24)

    # create common time labels for plots
    timelables = []
    for i in range(time_start, time_now, 60):
        utc = posix2utc(i)
        timelables.append(utc)

    index_satellites = create_satellite_dictionary()
    satellite_list = create_constellation(time_start, time_now)

    # only input data only if the satellite name exists in the satellite index,
    # and if the timestamps are in the range of time_start to time_now

    for entry in query:
        satname = entry[0]
        timevalue = entry[1]
        s4 = entry[4]
        # if the entry is in our index...
        if index_satellites.get(satname) is not None:
            # and the time value falls in the range
            satID = index_satellites.get(satname)
            if timevalue > time_start and timevalue < time_now:
                # set the update flag to true and add data to the satellites data store.
                satellite_list[satID].update_flag = True
                satellite_list[satID].name = satname
                satellite_list[satID].update_data(s4, timevalue)
            else:
                print("Satellite time value falls outside of range!!")
        else:
            print("Satellite ID does not exist in satellite index: " + str(entry[0]))

    plotlist = []
    for satellite in satellite_list:
        if satellite.update_flag is True:
            plotlist.append(satellite)

    plot(plotlist, timelables)




