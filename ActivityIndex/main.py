import time
from datetime import datetime
import binlibrary as binner
import heatmapconverter as hm

import importer

# ###############################################
# Main Parts STarts Here
# ###############################################
def do_main():
    importarray = importer.importdata("Dalmore_Prime.1minbins.csv")
    # importarray = importer.importdata()

    importarray.pop(0)
    print(importarray[10])

    # import the readings and convert to dH/dt
    dhdt = importarray
    dhdt = binner.make_dhdt(dhdt)

    # Convert the timestamps to UNIX
    dhdt = binner.utc2unix(dhdt)

    # Bin the data into appropriate intervals
    dhdt = binner.bin_dh_dt(dhdt)
    binner.SaveRawArray(dhdt, "output.csv")

    # Convert the binned data into colour-coded chart thing
    dhdt.reverse()
    dhdt = hm.main(dhdt)

    print("Binning complete.")
    print("\n")

# ###############################################
# recalculate the max min values once per 24hr
# ###############################################
def do_renormalise():
    pass

if __name__ == '__main__':
    starttime = datetime.now()
    starttime = time.mktime(starttime.timetuple())

    while True:
        #sleep time in seconds 86400sec in a day
        sleeptime = 900
        currenttime = datetime.now()
        currenttime = time.mktime(currenttime.timetuple())

        if currenttime > starttime + 86400:
            do_renormalise()
            starttime = currenttime
        else:
            do_main()
        time.sleep(sleeptime)