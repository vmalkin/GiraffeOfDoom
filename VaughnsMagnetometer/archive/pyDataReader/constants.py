__author__ = 'vaughn'

# Constants
MAG_READ_FREQ = 4           # how often the magnetometer sends data per minute
MAG_RUNNINGAVG_COUNT = 8   # for running averages
MAG3110_FLIP = 240          # Sensor chip flips at this reading

# Files
PATH_LOGS = 'logs/'
PATH_GRAPHING = 'graphing/'
FILE_ROLLING = 'ArraySave.csv'
FILE_24HR = 'graphing/24hr.csv'
FILE_4HR = "graphing/04hr.csv"
FILE_4DIFFS = "graphing/04diff.csv"
FILE_ERRORLOG = "Errors.log"

# Comm port parameters
portName = 'Com7'
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