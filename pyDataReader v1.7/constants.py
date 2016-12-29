__author__ = 'vaughn'

# Constants
MAG_READ_FREQ = 20           # how often the magnetometer sends data per minute
MAG_RUNNINGAVG_COUNT = 2   # The time in MINUTES that we want to average on. ONLY an even number
MAG3110_FLIP = 200          # Sensor chip flips at this reading
FIELD_CORRECTION = 1        # if the field is increasing in strength, the values should go up, and vica versa
STATION_ID = "Dalmore01."

# Files
PATH_LOGS = 'logs/'
PATH_GRAPHING = 'graphing/'
FILE_ROLLING = 'ArraySave.csv'
FILE_24HR = PATH_GRAPHING + "24hr.csv"
FILE_4HR = PATH_GRAPHING + "04hr.csv"
FILE_4DIFFS = PATH_GRAPHING + "diffs.csv"
FILE_ERRORLOG = "Errors.log"
FILE_BINNED_MINS = PATH_GRAPHING + STATION_ID + "1minbins.csv"

# Comm port parameters - uncomment and change one of the portNames depending on your OS
portName = 'Com8' # Windows
# portName = '/dev/tty.usbserial-A702O0K9' #MacOS
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
