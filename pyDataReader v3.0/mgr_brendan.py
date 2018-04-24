import time
import datapoint
import logging

errorloglevel = logging.DEBUG
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

class Data4Brendan():
    def __init__(self, data_array, mag_read_freq):
        self._data_array = data_array
        self._mag_read_freq = mag_read_freq

    def create_datablip(self):
        now_time = int(time.time())

        if len(self._data_array) > self._mag_read_freq:
            splitpoint = len(self._data_array) - self._mag_read_freq
            reduced_data = self._data_array[splitpoint:]

            avg_reading = 0.0
            for dataitem in reduced_data:
                avg_reading = avg_reading + float(dataitem.data_1)

            avg_reading = avg_reading / len(reduced_data)

            utctime = time.gmtime(now_time)
            utctime = time.strftime('%Y-%m-%d %H:%M:%S', utctime)

            # datavalue = utctime + "," + avg_reading
            datavalue = avg_reading

            try:
                with open("brendan.csv", 'w') as w:
                    w.write(str(datavalue) + '\n')
            except IOError:
                print("WARNING: There was a problem accessing brendan.csv")
                logging.warning("WARNING: File IO Exception raised whilst accessing file: brendan.csv")


