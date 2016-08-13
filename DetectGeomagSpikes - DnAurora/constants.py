__author__ = 'vaughn'

# Constants
# how often the magnetometer sends data per minute
MAG_READ_FREQ = 6
# MAG_RUNNINGAVG_COUNT = 12

# Level below which is background noise
MAG_THRESHOLD_NORMAL = 0.1
COLOUR_N = "#ACE5AC"
COLOUR_N_M = "#009d00"

# Level below which is background noise
MAG_THRESHOLD_MEDIUM = 0.2
COLOUR_M_H = "#e98830"

# Level over which is medium Activity.
MAG_THRESHOLD_HIGH = 0.4
COLOUR_H = "#e40707"

FIELD_CORRECTION = 1
MAG3110_FLIP = 200

# differences data from magnetometer
PATH_DATA = ""
FILE_BINNED_MINS = PATH_DATA + "diffs.csv"

# text output file
OUTPUT_PATH = ""
OUTPUT_FILE = OUTPUT_PATH + "geomag.php"