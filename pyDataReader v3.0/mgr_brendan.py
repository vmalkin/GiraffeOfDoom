import time
import logging
from decimal import Decimal, getcontext
getcontext().prec = 2

errorloglevel = logging.DEBUG
logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=errorloglevel)

class Data4Brendan():
    def __init__(self, data_array, mag_read_freq, field_correction):
        self._data_array = data_array
        self._mag_read_freq = mag_read_freq
        self._fieldcorrection = field_correction


    def create_datablip(self):
        t_now = int(time.time())
        t_prev = t_now - 60


        if len(self._data_array) > self._mag_read_freq:
            splitpoint = len(self._data_array) - (2* self._mag_read_freq)
            reduced_data = self._data_array[splitpoint:]

            templist = []
            for dataitem in reduced_data:
                if int(Decimal(dataitem.posix_time)) > int(t_prev) and int(Decimal(dataitem.posix_time)) <= int(t_now):
                    templist.append(dataitem.data_1)

            avg_reading = 0
            for item in templist:
                avg_reading = Decimal(avg_reading) + Decimal(item)

            avg_reading = (avg_reading / len(templist)) * self._fieldcorrection
            avg_reading = round(avg_reading, 2)

            utctime = time.gmtime(t_now)
            utctime = time.strftime('%Y-%m-%d %H:%M:%S', utctime)


            datavalue = str(utctime) + "," + str(avg_reading)
            # datavalue = avg_reading

            try:
                with open("../publish/brendan.csv", 'w') as w:
                    w.write(str(datavalue) + '\n')
            except IOError:
                print("WARNING: There was a problem accessing brendan.csv")
                logging.warning("WARNING: File IO Exception raised whilst accessing file: brendan.csv")


