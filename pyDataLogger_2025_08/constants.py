# Comm port parameters - uncomment and change one of the portNames depending on your OS
# portName = 'Com4' # Windows
# portName = '/dev/tty.usbserial-A702O0K9' #MacOS
# portName = "/dev/cu.usbmodem1421"
# portName = '/dev/ttyUSB0'
comport = "/dev/ttyACM0"
# comport = "/dev/ttyACM1"
baudrate = 9600
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

sensor = "BMP 280 Pressure Sensor"
dir_images = "images"
dir_logfiles = "logfiles"
