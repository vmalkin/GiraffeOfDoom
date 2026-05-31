# from numpy import nan
# Comm port parameters - uncomment and change one of the portNames depending on your OS
# comport = 'COM5' # Windows
# portName = '/dev/tty.usbserial-A702O0K9' #MacOS
# portName = "/dev/cu.usbmodem1421"
# comport = '/dev/ttyUSB0'
# comport = "/dev/ttyACM0"
# comport = "/dev/ttyACM1"
# baudrate = 57600
# bytesize = 8
# parity = 'N'
# stopbits = 1
# timeout = 60
# xonxoff = False
# rtscts = True
# writeTimeout = None
# dsrdtr = False
# interCharTimeout = None

timeformat = '%Y-%m-%d %H:%M:%S'
database = 'tiltmeter.db'

sensor = "Logitech_C270"
# How many times a second the sensor reports data to the logger
sensor_reading_frequency = 30
# Buffer length is for 30 mins plus 10%
buffer_length = int((sensor_reading_frequency * 60 * 30) * 1.1)

dir_saves = {
    'logs': 'logfiles'
}
