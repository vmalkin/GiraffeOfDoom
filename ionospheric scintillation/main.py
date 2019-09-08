import pickle
import constants as k
import mgr_comport
import mgr_satellites

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
    print(com.data_recieve())