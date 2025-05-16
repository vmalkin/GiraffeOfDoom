import serial
import logging
import sys
# errorloglevel = logging.DEBUG
# logging.basicConfig(filename="comport.log", format='%(asctime)s %(message)s', level=errorloglevel)


class SerialManager:
    def __init__(self, portName, baudrate, bytesize, parity, stopbits, timeout, xonxoff,
                 rtscts, writeTimeout, dsrdtr, interCharTimeout):
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
            self.com = serial.Serial(self._portName, self._baudrate, self._bytesize, self._parity, self._stopbits,
                                     self._timeout, self._xonxoff, self._rtscts, self._writeTimeout,
                                     self._dsrdtr, self._interCharTimeout)
        except serial.SerialException:
            print("CRITICAL ERROR: Com port not responding. Please check parameters")
            # logging.critical("CRITICAL ERROR: Unable to open com port. Please check com port parameters and/or hardware!!")
            print("\n\n" + str(sys.exc_info()))

    def data_recieve(self):
        try:
            logData = self.com.readline()  # logData is a byte array, not a string at this point
            # logData = str(logData, 'ascii').strip()  # convert the byte array to string. strip off unnecessary whitespace
            logData = str(logData, 'latin1').strip()  # convert the byte array to string. strip off unnecessary whitespace
        except serial.serialutil.SerialException:
            logData = ""
            # logging.error("Serial port error " + str(serial.serialutil.SerialException))
        return logData