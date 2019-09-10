import pickle
import constants as k
import mgr_comport
import mgr_satellites
import time
from threading import Thread
import sys

gpgsv = 100
glgsv = 200
max_array = 310
constellation = []

class SatelliteCollator(Thread):
    def __init__(self):
        Thread.__init__(self, name="SatelliteCollator")
    def run(self):
        while True:
            print("Satellite List Size: " + str(sys.getsizeof(constellation)))

            time.sleep(60)

# aliases for the different constellations so we can make a hash table.


for i in range(100, max_array):
    sat = mgr_satellites.Satellite()
    constellation.append(sat)

com = mgr_comport.SerialManager(k.portName,k.baudrate, k.bytesize, k.parity, k.stopbits, k.timeout, k.xonxoff, k.rtscts, k.writeTimeout, k.dsrdtr, k.interCharTimeout)

if __name__ == "__main__":
    sat_collation = SatelliteCollator()
    try:
        sat_collation.start()
    except:
        print("Unable to start Satellite Collator")

    while True:
        # $GLGSV,3,1,10,68,09,163,,69,33,118,,70,25,051,,74,08,348,*62
        # ['GLGSV', '76', '48', '296', '41', '77', '32', '221', '18', '85', '36', '123', '18', '86', '62', '219', '29']
        line = com.data_recieve()
        line = line[1:]
        line = line[:-3]
        line = line.split(",")
        # Remove non satellite data from sentence
        if len(line) > 1:
            line.pop(1)
            line.pop(1)
            line.pop(1)
        posix_time = time.time()

        prefix = ""
        if line[0] == "GPGSV":
            prefix = gpgsv
        if line[0] == "GLGSV":
            prefix = glgsv

        try:
            s1_nam = line[1]
            # s1_alt = line[2]
            # s1_azm = line[3]
            # s1_snr = line[4]
            constellation[prefix + s1_nam].speak(prefix + s1_nam)
        except:
            print("Unable to add satellite " + str(prefix) + "No 1")

        try:
            s2_nam = line[5]
            # s2_alt = line[6]
            # s2_azm = line[7]
            # s2_snr = line[8]
            constellation[prefix + s2_nam].speak(prefix + s2_nam)
        except:
            print("Unable to add satellite " + str(prefix) + "No 2")

        try:
            s3_nam = line[9]
            # s3_alt = line[10]
            # s3_azm = line[11]
            # s3_snr = line[12]
            constellation[prefix + s3_nam].speak(prefix + s3_nam)
        except:
            print("Unable to add satellite " + str(prefix) + "No 3")

        try:
            s4_nam = line[13]
            # s4_alt = line[14]
            # s4_azm = line[15]
            # s4_snr = line[16]
            constellation[prefix + s4_nam].speak(prefix + s4_nam)
        except:
            print("Unable to add satellite " + str(prefix) + "No 4")
