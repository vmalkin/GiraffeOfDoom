__author__ = 'vaughn'

# Constants
# how often the magnetometer sends data per minute
MAG_READ_FREQ = 4
# MAG_RUNNINGAVG_COUNT = 12


# differences data from magnetometer
PATH_DATA = "../pyDataReader/graphing/"
FILE_BINNED_MINS = PATH_DATA + "diffs.csv"

# text output file
OUTPUT_PATH = "../pyDataReader/publish/"
OUTPUT_FILE = OUTPUT_PATH + "geomag.php"