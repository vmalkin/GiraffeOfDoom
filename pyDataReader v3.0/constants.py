mag_read_freq = 30   # how many readings per minute
mag_running_count = 6
noise_spike = 500   # threshold for rate of change noise
field_correction = 1   # graph should go up, as H value increases
station_id = "dna_fgm_1"   # ID of magnetometer station
FILE_4DIFFS = "diffs.csv"
publish_folder = "publish"

# Comm port parameters - uncomment and change one of the portNames depending on your OS
portName = 'Com17' # Windows
# portName = '/dev/tty.usbserial-A702O0K9' #MacOS
# portName = '/dev/ttyUSB0'
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
