import constants as k
import ArrayManager as am
from decimal import Decimal, getcontext
import os
import time
import binlibrary as binner

# append output to a file.
def createoutputfile(texttowrite, filename):
    try:
        with open(filename, 'a') as f:
            f.write(texttowrite + "\n")
    except IOError:
        print("WARNING: There was a problem accessing " + k.OUTPUT_FILE)



# ###############################################
# Main Parts STarts Here
# ###############################################

while True:
    try:
        importarray = []
        # Load up file into array
        # print(k.FILE_BINNED_MINS)
        importarray = am.CreateRawArray(k.FILE_BINNED_MINS)

        # remove the first line which may contain text header
        importarray.pop(0)

        # create the bins for dh/dt
        importarray = binner.utc2unix(importarray)
        importarray = binner.bin_dh_dt(importarray)
        importarray = binner.unix2utc(importarray)





    except:
        print("The Binning Program has failed for some general reason")

    time.sleep(600)