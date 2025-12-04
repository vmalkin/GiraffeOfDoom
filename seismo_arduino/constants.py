# Comm port parameters - uncomment and change one of the portNames depending on your OS
# comport = 'Com6' # Windows
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
sat_database = "data.db"

sensor = "Tilt Meter Sensor"
sensor_reading_frequency = 1 / 10
dir_images = ['images', 'phaseplots', 'spectrograms']
dir_logfiles = "logfiles"
