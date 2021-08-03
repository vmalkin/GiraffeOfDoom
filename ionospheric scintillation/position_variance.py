import serial
from threading import Thread
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Comm port parameters - uncomment and change one of the portNames depending on your OS
portName = 'Com39' # Windows
# portName = '/dev/tty.usbserial-A702O0K9' #MacOS
# portName = "/dev/cu.usbmodem1421"
# portName = '/dev/ttyUSB0'
# baudrate = 9600 # for SAM module at DUnedin Aurora
baudrate = 57600
bytesize = 8
parity = 'N'
stopbits = 1
timeout = 60
xonxoff = False
rtscts = True
writeTimeout = None
dsrdtr = False
interCharTimeout = None


class SerialManager():
    def __init__(self, portName,baudrate,bytesize,parity,stopbits,timeout,xonxoff,rtscts,writeTimeout,dsrdtr,interCharTimeout):
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
                plot_graph(master_array)
            except:
                print("Failed plot")
            time.sleep(600)

def parse_date(ut_date, ut_time):
    # 030821, 082434.000
    day = ut_date[:2]
    month = ut_date[2:4]
    year = "20" + ut_date[4:]
    hour = ut_time[:2]
    min = ut_time[2:4]
    sec = ut_time[4:6]
    dt = year + "-" + month + "-" + day + " " + hour + ":" + min + ":" + sec
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
    d = np.array(data)
    dates = (d[:,0])
    lat = (d[:,1])
    long = (d[:,2])

    filename = dates[len(dates) - 1]
    filename = filename.split(" ")
    filename = str(filename[0]) + ".jpg"

    # lat_clr = "red"
    # long_clr = "blue"

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=dates, y=lat, name="Latitude"),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(x=dates, y=long, name="Longtiude"),
        secondary_y=True
    )

    fig.update_layout(width=1800, height=600, title="GPS variations (decimal part)")
    #
    # fig.update_yaxes(title_text="Latitude", secondary_y=False, font=dict(color=lat_clr))
    # fig.update_yaxes(title_text="Longtiude", secondary_y=True, font=dict(color=long_clr))
    fig.write_image(file=filename, format="jpg")
    fig.show()

if __name__ == "__main__":
    master_array = []
    lat_old = float(0)
    long_old = float(0)
    start_flag = False

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
        if data[1] == "G":
            if data[2] == "P":
                if data[3] == "R":
                    # print(data)
                    try:
                        data = data.split(",")
                        ut_time = data[1]
                        ut_date = data[9]
                        lat = float(data[3])
                        long = float(data[5])

                        if start_flag == True:
                            lat = process_lats(lat)
                            long = process_longs(long)
                            utcdate = parse_date(ut_date, ut_time)
                            datapoint = [utcdate, lat ,long]
                            print(datapoint)
                            master_array.append(datapoint)

                            if len(master_array) > maxlen:
                                master_array.pop(0)

                        if start_flag == False:
                            start_flag = True
                            lat_old = lat
                            long_old = long
                    except:
                        print("Malformed NMEA sentence")



