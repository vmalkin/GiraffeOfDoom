import serial
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
import logging
import os
import datetime
import calendar
from statistics import median
from threading import Thread


db = "positions.db"
errorloglevel = logging.DEBUG
logging.basicConfig(filename="position_errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

# Comm port parameters - uncomment and change one of the portNames depending on your OS
portName = 'Com39'  # Windows
# portName = '/dev/tty.usbserial-A702O0K9' #MacOS
# portName = "/dev/cu.usbmodem1421"
# portName = '/dev/ttyUSB0'
# baudrate = 9600 # for SAM module at DUnedin Aurora
baudrate = 115200
bytesize = 8
parity = 'N'
stopbits = 1
timeout = 60
xonxoff = False
rtscts = True
writeTimeout = None
dsrdtr = False
interCharTimeout = None


class SerialManager:
    def __init__(self, portName, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts, writeTimeout, dsrdtr, interCharTimeout):
        self._portName = portName
        self._baudrate = baudrate
        self._bytesize = bytesize
        self._parity = parity
        self._stopbits = stopbits
        self._timeout = timeout
        self._xonxoff = xonxoff
        self._rtscts = rtscts
        self._writeTimeout = writeTimeout
        self._dsrdtr = dsrdtr
        self._interCharTimeout = interCharTimeout

        try:
            self.com = serial.Serial(self._portName, self._baudrate, self._bytesize, self._parity, self._stopbits, self._timeout, self._xonxoff,
                                     self._rtscts, self._writeTimeout, self._dsrdtr, self._interCharTimeout)
        except serial.SerialException:
            print("CRITICAL ERROR: Com port not responding. Please check parameters")

    def data_recieve(self):
        try:
            logData = self.com.readline()  # logData is a byte array, not a string at this point
            # logData = str(logData, 'ascii').strip()  # convert the byte array to string. strip off unnecessary whitespace
            logData = str(logData, 'latin1').strip()  # convert the byte array to string. strip off unnecessary whitespace
        except serial.serialutil.SerialException:
            print("Unable to read com port")
        return logData


class ThreadPlotter(Thread):
    def __init__(self):
        Thread.__init__(self, name="QueryProcessor")

    def run(self):
        while True:
            try:
                data = database_getdata(db)
                plot_graph(data)
            except:
                print("Failed plot")
            time.sleep(600)


def create_directory(dirs):
    try:
        os.makedirs(dirs)
        print("Directory created.")
    except:
        if not os.path.isdir(dirs):
            print("Unable to create directory")
            logging.critical("CRITICAL ERROR: Unable to create directory in MAIN.PY")


def database_create(database):
    if os.path.isfile(database) is False:
        print("No database, creating file")
        gpsdb = sqlite3.connect(database)
        db = gpsdb.cursor()
        db.execute('drop table if exists satdata;')
        db.execute('create table satdata ('
                   'posixtime string,'
                   'var_lat real,'
                   'var_long real'
                   ');')
        gpsdb.commit()
        db.close()


def database_append(database, posixdate, lats, longs):
    gpsdb = sqlite3.connect(database)
    db = gpsdb.cursor()
    db.execute("insert into satdata (posixtime, var_lat, var_long) "
               "values(?, ?, ?)", [posixdate, lats, longs])
    gpsdb.commit()
    db.close()


def database_getdata(database):
    fromdate = int(time.time() - (60 * 60 * 24))
    gpsdb = sqlite3.connect(database)
    db = gpsdb.cursor()
    result = db.execute("select * from satdata where satdata.posixtime > ? order by posixtime asc", [fromdate])

    returnlist = []
    for item in result:
        dp = (item[0], item[1], item[2])
        returnlist.append(dp)
    print("current query " + str(len(returnlist)) + " records long")

    gpsdb.commit()
    db.close()
    return returnlist


def posix2utc(posixtime, timeformat):
    # timeformat = '%Y-%m-%d %H:%M:%S'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def utc2posix(utc_time):
    timeformat = '%Y-%m-%d %H:%M:%S'
    date_obj = datetime.datetime.strptime(utc_time, timeformat)
    posixtime = calendar.timegm(date_obj.timetuple())
    return posixtime


def parse_date(ut_date, ut_time):
    # 030821, 082434.000
    day = ut_date[:2]
    month = ut_date[2:4]
    year = "20" + ut_date[4:]
    hour = ut_time[:2]
    mins = ut_time[2:4]
    sec = ut_time[4:6]
    dt = year + "-" + month + "-" + day + " " + hour + ":" + mins + ":" + sec
    return dt


def process_lats(lat):
    d = float(lat - 4552)
    d = round(d, 6)
    return d


def process_longs(long):
    d = float(long - 17029)
    d = round(d, 6)
    return d


def plot_graph(data):
    dates = []
    lat = []
    long = []

    for dp in data:
        dates.append(posix2utc(dp[0], '%Y-%m-%d %H:%M:%S'))
        lat.append(dp[1])
        long.append(dp[2])

    filename = posix2utc(time.time(), '%Y-%m-%d')
    filename = filename + ".jpg"

    lat_clr = "red"
    long_clr = "blue"

    fig = make_subplots(rows=2, cols=1, subplot_titles=("Variance in Latitude", "Variance in Longtitude"))
    fig.add_trace(go.Scatter(x=dates, y=lat, mode="lines", line=dict(width=2, color=lat_clr)), row=1, col=1)
    fig.add_trace(go.Scatter(x=dates, y=long, mode="lines", line=dict(width=2, color=long_clr)), row=2, col=1)
    fig.update_xaxes(nticks=30, tickangle=45)
    fig.update_layout(font=dict(size=20), title_font_size=21)
    fig.update_layout(width=2000, height=1000,
                      title="GPS variations (decimal part)",
                      showlegend=False, plot_bgcolor="#a0a0a0", paper_bgcolor="#a0a0a0")

    fig.write_image(file=filename, format="jpg")
    # fig.show()


if __name__ == "__main__":
    master_array = []
    all_lats = []
    all_longs = []
    lat_old, long_old = 0.0, 0.0
    start_flag = False

    # check/create the database
    database_create(db)

    plotter = ThreadPlotter()
    try:
        plotter.start()
        print("Starting plotter thread...")
    except:
        print("Plotter thread failed!")

    com = SerialManager(portName,
                        baudrate,
                        bytesize,
                        parity,
                        stopbits,
                        timeout,
                        xonxoff,
                        rtscts,
                        writeTimeout,
                        dsrdtr,
                        interCharTimeout)

    while True:
        maxlen = 60 * 60 * 24
        data = com.data_recieve()
        if data[0] == '$':
            if data[1] == 'G':
                if data[2] == 'P':
                    # print(data)
                    try:
                        data = data.split(",")
                        ut_time = data[1]
                        ut_date = data[9]
                        lat = float(data[3])
                        long = float(data[5])

                        newlat = process_lats(lat)
                        newlong = process_longs(long)

                        all_lats.append(newlat)
                        all_longs.append(newlong)

                        if len(all_lats) >= 60:
                            if start_flag is False:
                                median_lat = median(all_lats)
                                median_long = median(all_longs)

                                lat_old = median_lat
                                long_old = median_long
                                start_flag = True
                            else:
                                median_lat = median(all_lats)
                                median_long = median(all_longs)
                                utcdate = parse_date(ut_date, ut_time)
                                posixdate = utc2posix(utcdate)

                                # Calculate the rate of change
                                variance_lat_new = round((median_lat - lat_old), 7)
                                variance_long_new = round((median_long - long_old), 7)

                                datapoint = [utcdate, variance_lat_new, variance_long_new]
                                print(datapoint)

                                database_append(db, posixdate, variance_lat_new, variance_long_new)

                                # master_array.append(datapoint)

                                all_lats = []
                                all_longs = []
                                lat_old = median_lat
                                long_old = median_long

                        if len(master_array) > maxlen:
                            master_array.pop(0)

                    except:
                        print("Malformed NMEA sentence")
                        logging.debug(data)