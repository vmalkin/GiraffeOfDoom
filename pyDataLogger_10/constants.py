# global constants and configuration information
# Database, Station ID and file/folders
station_id = "ruru"   # ID of magnetometer station
database = "arraysave.db"
logfile_dir = "dailylogs"
publish_dir = "publish"

# The number of readings per minute the device spits out
device_rpm = 60

# Comm port parameters - uncomment and change one of the portNames depending on your OS
# portName = 'Com42'   # Windows
# portName = '/dev/tty.usbserial-A9MO3C9T'   #MacOS
portName = '/dev/ttyUSB0'   # Linux
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

# Plotly graphing parameters
plot_width = 1500
plot_height = 500
plot_backgroundcolour = "#ffffff"
plot_pencolour = "#600000"
plot_gridcolour = "#909090"