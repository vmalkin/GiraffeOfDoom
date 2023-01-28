# Comm port parameters - uncomment and change one of the portNames depending on your OS
# portName = 'Com3' # Windows
# portName = '/dev/tty.usbserial-A702O0K9' #MacOS
# portName = "/dev/cu.usbmodem1421"
# portName = '/dev/ttyUSB0'
port1 = "/dev/ttyACM0"
port2 = "/dev/ttyACM1"
baudrate = 115200
bytesize = 8
parity = 'N'
stopbits = 1
timeout = 60
xonxoff = False
rtscts = True
writeTimeout = None
dsrdtr = False
interCharTimeout = None

sensor = "UBlox"
dir_images = "images"
dir_logfiles = "logfiles"
