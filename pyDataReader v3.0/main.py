import mgr_data
import mgr_files
import mgr_serialport

# Constants and other global variables required
MAG_READ_FREQ = 30         # how often the magnetometer sends data per minute
MAG_RUNNINGAVG_COUNT = 6   # The number of readings "wide" the averaging window is. EVEN NUMBER
NOISE_SPIKE = 2          # Sensor chip flips at this reading
FIELD_CORRECTION = -1        # if the field is increasing in strength, the values should go up, and vica versa
STATION_ID = "RuruRapid."

# Comm port parameters - uncomment and change one of the portNames depending on your OS
# portName = 'Com4' # Windows
# portName = '/dev/tty.usbserial-A702O0K9' #MacOS
portName = '/dev/ttyACM0'
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


if __name__ == "__main__":
    pass
    