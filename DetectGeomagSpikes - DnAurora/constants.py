__author__ = 'vaughn'

# Constants
# how often the magnetometer sends data per minute
MAG_READ_FREQ = 6
# MAG_RUNNINGAVG_COUNT = 12

FIELD_CORRECTION = 1
MAG3110_FLIP = 200

# differences data from magnetometer
PATH_DATA = ""
FILE_BINNED_MINS = PATH_DATA + "diffs.csv"

# text output file
OUTPUT_PATH = ""
OUTPUT_FILE = OUTPUT_PATH + "geomag.php"