import pickle
import constants as k
import mgr_comport
import mgr_satellites
import re

# aliases for the different constellations so we can make a hash table.
gpgsv = 100
glgsv = 200
max_array = 310
constellation = []

for i in range(0, max_array):
    sat = mgr_satellites.Satellite()
    constellation.append(sat)

com = mgr_comport.SerialManager(k.portName,k.baudrate, k.bytesize, k.parity, k.stopbits, k.timeout, k.xonxoff, k.rtscts, k.writeTimeout, k.dsrdtr, k.interCharTimeout)

while __name__ == "__main__":
    # $GLGSV,3,1,10,68,09,163,,69,33,118,,70,25,051,,74,08,348,*62
    line = com.data_recieve()
    line = line[1:]
    line = line[:-3]
    line = line.split(",")
    # Remove non satellite data from sentence
    if len(line) > 1:
        line.pop(1)
        line.pop(1)
        line.pop(1)
    print(line)
