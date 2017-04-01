import constants as k
import ArrayManager as am
import time
import binlibrary as binner
import heatmapconverter as hm

import importer

# ###############################################
# Main Parts STarts Here
# ###############################################

while True:
    importarray = importer.importdata()

    importarray.pop(0)
    print(importarray[10])

    # import the readings and convert to dH/dt
    dhdt = importarray
    dhdt = binner.make_dhdt(dhdt)

    # smooth data if necessary
    dhdt = binner.running_average(dhdt)
    dhdt = binner.running_average(dhdt)

    # Convert the timestamps to UNIX
    dhdt = binner.utc2unix(dhdt)

    # Bin the data into appropriate intervals
    dhdt = binner.bin_dh_dt(dhdt)
    binner.SaveRawArray(dhdt,"output.csv")

    # Convert the binned data into colour-coded chart thing
    dhdt.reverse()
    dhdt = hm.main(dhdt)

    print("Binning complete.")
    print("\n")

    # tap our data as infrequently as we can get away with
    time.sleep(900)