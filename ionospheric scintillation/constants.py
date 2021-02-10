# Comm port parameters - uncomment and change one of the portNames depending on your OS
portName = 'Com10' # Windows
# portName = '/dev/tty.usbserial-A702O0K9' #MacOS
# portName = "/dev/cu.usbmodem1421"
# portName = '/dev/ttyUSB0'
# baudrate = 9600 # for SAM module at DUnedin Aurora
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

imagesdir = "images"
logfiledir = "logfiles"
