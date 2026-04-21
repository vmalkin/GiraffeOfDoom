# from numpy import nan
# Comm port parameters - uncomment and change one of the portNames depending on your OS
# comport = 'COM5' # Windows
# portName = '/dev/tty.usbserial-A702O0K9' #MacOS
# portName = "/dev/cu.usbmodem1421"
# comport = '/dev/ttyUSB0'
comport = "/dev/ttyACM0"
# comport = "/dev/ttyACM1"
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

timeformat = '%Y-%m-%d %H:%M:%S'
database = 'weather_data.db'

sensor = "BMP280"
# How many times a second the sensor reports data to the logger
sensor_reading_frequency = 1
# deque buffer length is for 24 hours plus 10%
buffer_length = int((24 * 60 * 60 * sensor_reading_frequency) * 1.1)

dir_saves = {
    'logs': 'logfiles'
}
