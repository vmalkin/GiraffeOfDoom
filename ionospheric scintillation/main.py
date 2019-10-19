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
            pass
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

    print("Starting GPS collection...")


    while True:
        count  = 0
        while count <= 60:
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
                s1_nam = int(line[1])
                s1_alt = int(line[2])
                s1_azm = int(line[3])
                s1_snr = int(line[4])
                constellation[prefix + s1_nam].list_posix.append(posix_time)
                constellation[prefix + s1_nam].list_altitude.append(s1_alt)
                constellation[prefix + s1_nam].list_azimuth.append(s1_azm)
                constellation[prefix + s1_nam].list_snr.append(s1_snr)
            except:
                pass

            try:
                s2_nam = int(line[5])
                s2_alt = int(line[6])
                s2_azm = int(line[7])
                s2_snr = int(line[8])
                constellation[prefix + s2_nam].list_posix.append(posix_time)
                constellation[prefix + s2_nam].list_altitude.append(s2_alt)
                constellation[prefix + s2_nam].list_azimuth.append(s2_azm)
                constellation[prefix + s2_nam].list_snr.append(s2_snr)
            except:
                pass

            try:
                s3_nam = int(line[9])
                s3_alt = int(line[10])
                s3_azm = int(line[11])
                s3_snr = int(line[12])
                constellation[prefix + s3_nam].list_posix.append(posix_time)
                constellation[prefix + s3_nam].list_altitude.append(s3_alt)
                constellation[prefix + s3_nam].list_azimuth.append(s3_azm)
                constellation[prefix + s3_nam].list_snr.append(s3_snr)
            except:
                pass

            try:
                s4_nam = int(line[13])
                s4_alt = int(line[14])
                s4_azm = int(line[15])
                s4_snr = int(line[16])
                constellation[prefix + s4_snr].list_posix.append(posix_time)
                constellation[prefix + s4_snr].list_altitude.append(s4_alt)
                constellation[prefix + s4_snr].list_azimuth.append(s4_azm)
                constellation[prefix + s4_snr].list_snr.append(s4_snr)
            except:
                pass

            count = count + 1

        for satellite in constellation:
            satellite.satellite_print_values()
            satellite.list_posix = []
            satellite.list_snr = []
            satellite.list_altitude = []
            satellite.list_azimuth = []
        print("Satellites reset for next count")

