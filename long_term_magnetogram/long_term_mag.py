import time
from plotly import graph_objects as go
import standard_stuff as k
from os import path
from statistics import median, mean
import re


# Index positions of UTC date and data in each logfile. This could be different...
regex_filename = "\d\d\d\d-\d\d-\d\d.csv"
rounding_value = 5
# Positions for markers
value_base = -0.005
value_step = 0.01
value_cmarker = value_base + value_step
value_equinox = value_cmarker + value_step
value_storm = value_equinox + value_step
value_sighting = value_storm + value_step
value_cme = value_sighting + value_step




# Create a bin object. A bin:
# Covers a time period
# Has a list of data values for the time period
# Identifies if there was a magnetic storm for the time period
# Identifies if there were sightings recorded for the time period
# Can output time and data values as CSV formatted string.
# Can return a CSV formatted header for data
class Bin:
    def __init__(self, time):
        self.storm_threshhold = 0.09
        self.time = time
        self.data = []
        self.sighting = None
        self.carrington_marker = None
        self.equinox = None
        self.cme = None

    def dhdt(self):
        if len(self.data) > 0:
            value = round((max(self.data) - min(self.data)), rounding_value)
        else:
            value = 0
        return value

    def storm_detected(self):
        if self.dhdt() >= self.storm_threshhold:
            return value_storm
        else:
            return None


def median_filter(list_to_parse):
    # Each element in the list has the format [datetime, data]
    # The half window value should cover 10 minutes of data
    returnlist = []
    halfwindow = 5 * 4
    for i in range(halfwindow, len(array_time_data) - halfwindow):
        # print("Smoothing " + str(i) + " out of " + str(len(array_time_data)))
        d = []
        for j in range(0 - halfwindow, halfwindow):
            if j == 0:
                tt = array_time_data[i + j][0]
            d.append(array_time_data[i + j][1])
        dd = median(d)
        dp = [tt, dd]
        returnlist.append(dp)
    return returnlist


def h_to_dhdt(array_time_data):
    returnlist = []
    for i in range(1, len(array_time_data)):
        tt = array_time_data[i][0]
        dh = array_time_data[i][1] - array_time_data[i - 1][1]
        dh = round(dh, rounding_value)
        dp = [tt, dh]
        returnlist.append(dp)
    return returnlist


def smooth_data(array_time_data):
    # Each element in the list has the format [datetime, data]
    # The half window value should cover 10 minutes of data
    decade = int(len(array_time_data) / 10)
    decadecount = 0
    returnlist = []
    halfwindow = 30 * 4
    for i in range(halfwindow, len(array_time_data) - halfwindow):
        if i % decade == 0:
            decadecount = decadecount + 10
            print("Smoothing " + str(decadecount) + "% completed")
        # print("Smoothing " + str(i) + " out of " + str(len(array_time_data)))
        d = []
        for j in range(0 - halfwindow, halfwindow):
            if j == 0:
                tt = array_time_data[i + j][0]
            d.append(array_time_data[i + j][1])
        dd = mean(d)
        dp = [tt, dd]
        returnlist.append(dp)
    return returnlist


def plot(dates, dhdt, storm, sighting, carrington_marks, equinox_marks, cme):
    plot_width = 1800
    plot_height = 750
    bgcolor = "#e0e0e0"
    fig = go.Figure(data=[go.Bar(x=dates, y=dhdt, name="Geomagnetic Activity", marker_color="lightslategrey")])
    fig.update_layout(width=plot_width, height=plot_height,
                      legend=dict(orientation="h", xanchor="center", x=0.5),
                      plot_bgcolor=bgcolor, paper_bgcolor=bgcolor,
                      font=dict(color="#303030", size=16),
                      title="Long Term Magnetogram")
    fig.update_xaxes(nticks=24, tickangle=25, ticks="outside", tickwidth=2, tickcolor='black', ticklen=5)
    fig.update_yaxes(range=[0, 0.2])
    fig.add_scatter(x=dates, y=storm, mode='markers', name="Storm Detected",
                    marker_symbol=22, marker_line_color="darkred",
                    marker_color="red", marker_line_width=2, marker_size=10)
    fig.add_scatter(x=dates, y=sighting, mode='markers', name="Aurora Sighted",
                    marker_symbol=23, marker_line_color="darkgreen",
                    marker_color="green", marker_line_width=2, marker_size=10)
    fig.add_scatter(x=dates, y=carrington_marks, mode='markers', name="Carrington Rotation",
                    marker_symbol=20, marker_color="black", marker_size=10)
    fig.add_scatter(x=dates, y=equinox_marks, mode='markers', name="Equinox",
                    marker=dict(size=12, color="orange", line=dict(width=2, color='red')))
    fig.add_scatter(x=dates, y=cme, mode='markers', name="CME",
                    marker_symbol=17, marker_line_color="blue",
                    marker_color="cyan", marker_line_width=2, marker_size=10)
    fig.write_image("ltm.svg")
    fig.write_html("ltm.html")
    # fig.show()


if __name__ == '__main__':
    regex_data = "/d/d/d/d-/d/d-/d/d /d/d:/d/d:/d/d./d/d"
    array_time_data = []
    nowdate = int(time.time())
    startdate = nowdate - 86400 * 365

    # does files.txt exist? if not, abort
    if path.exists(k.file_list):
        # load files.txt
        with open(k.file_list, "r") as filelist:
            print("Loading values from files...")
            for filename in filelist:
                nw_filename = filename.strip()
                if re.match(regex_filename, nw_filename):
                    # Only process files for the last year, not older.
                    x = nw_filename.split(".")
                    xt = k.utc2posix(x[0], "%Y-%m-%d")
                    if xt >= startdate:
                        # open each file in the list
                        # parse thru each file, extract date and data value. If valid assemble into master list
                        with open(nw_filename, "r") as csvdata:
                            for csvline in csvdata:
                                newcsv = csvline.strip()
                                newcsv = newcsv.split(",")
                                # If we have data and not a header
                                tt = newcsv[0]
                                dd = newcsv[1]

                                if tt != "Date/Time (UTC)":
                                    try:
                                        posixtime = k.utc2posix(newcsv[0], "%Y-%m-%d %H:%M:%S.%f")
                                        data = float(newcsv[1])
                                        dp = [posixtime, data]
                                        array_time_data.append(dp)
                                    except ValueError:
                                        print(newcsv[0])

        # Remove any spikes in data with a median filter.
        print("Removing spikes in data...")
        array_time_data = median_filter(array_time_data)

        # smooth the data
        print("Smoothing data, this will take a while...")
        array_time_data = smooth_data(array_time_data)

        # Convert the data into dh/dt
        print("Converting to dh/dt...")
        array_time_data = h_to_dhdt(array_time_data)

        # Create a series of 365 dated bins for the previous 365 days
        print("Creating bins...")

        array_year = []
        for i in range(365, 0, -1):
            d = nowdate - i * 86400
            array_year.append(Bin(d))

        print("Populating bin arrays...")
        # parse thru the list and allocate data values to bins (each bin will have a list of data for the day)
        for item in array_time_data:
            tt = item[0]
            dd = item[1]
            index = int((tt - startdate) / 86400)
            if index >= 0:
                array_year[index].data.append(dd)

        print("Adding sightings to bins...")
        # open the sightings file. allocate the dates of sightings to each bin.
        with open("sightings.csv", "r") as s:
            for line in s:
                t = line.strip()
                # regex_dt = "/d/d-/d/d-/d/d/d/d"
                # if re.match(regex_dt, t):
                try:
                    tt = k.utc2posix(t, "%d-%m-%Y")
                    index = int((tt - startdate) / 86400)
                    if index >= 0:
                        if index < 365:
                            array_year[index].sighting = value_sighting
                except ValueError:
                    print(t)

        # Add carrington rotation marker
        for i in range(0, 365):
            if i % 27 == 0:
                array_year[i].carrington_marker = value_cmarker

        # Add solstice markers
        for item in array_year:
            if k.posix2utc(item.time, "%m-%d") == "03-20":
                item.equinox = value_equinox
            if k.posix2utc(item.time, "%m-%d") == "09-21":
                item.equinox = value_equinox

        # Add markers for CMEs
        print("Adding CMEs to bins...")
        # open the sightings file. allocate the dates of sightings to each bin.
        with open("cme.csv", "r") as s:
            for line in s:
                t = line.strip()
                # regex_dt = "/d/d-/d/d-/d/d/d/d"
                # if re.match(regex_dt, t):
                try:
                    tt = k.utc2posix(t, "%d-%m-%Y")
                    index = int((tt - startdate) / 86400)
                    if index >= 0:
                        if index < 365:
                            array_year[index].cme = value_cme
                except ValueError:
                    print(t)

        # with open("aurora_activity.csv", "w") as l:
        #     l.write("Date/Time(UTC), Geomagnetic Activity, Storm Detected, Aurora Sighted, Carrington Rotation Marker" + "\n")
        #     for item in array_year:
        #         dp = k.posix2utc(item.time, "%Y-%m-%d") + "," + str(item.dhdt()) + "," + \
        #              str(item.storm_detected()) + "," + str(item.sighting) + "," + str(item.carrington_marker)
        #         l.write(dp + "\n")
        # l.close()

        dates = []
        dhdt = []
        storm = []
        sighting = []
        carrington_marks = []
        equinox_marks = []
        cme = []

        for item in array_year:
            dates.append(k.posix2utc(item.time, "%Y-%m-%d"))
            dhdt.append(item.dhdt())
            storm.append(item.storm_detected())
            sighting.append(item.sighting)
            carrington_marks.append(item.carrington_marker)
            equinox_marks.append(item.equinox)
            cme.append(item.cme)

        plot(dates, dhdt, storm, sighting, carrington_marks, equinox_marks, cme)
        print("FINSIHED!")

    else:
        print("FILES.TXT does not exists. Create list of log files then rerun this script.")
