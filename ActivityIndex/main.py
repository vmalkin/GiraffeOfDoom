import constants as k
import ArrayManager as am
import time
import binlibrary as binner
import heatmapconverter as hm


# ###############################################
# Main Parts STarts Here
# ###############################################

while True:
    importarray = []
    # Load up file into array
    # print(k.INPUT_FILE)
    importarray = am.CreateRawArray(k.INPUT_FILE)

    # remove the first line which may contain text header
    importarray.pop(0)

    # create the bins for dh/dt
    dhdt = importarray

    # Convert the timestamps to UNIX
    dhdt = binner.utc2unix(dhdt)

    # Calculate dH/dt from the absolute readings of the magnetometer
    dhdt = binner.bin_dh_dt(dhdt)

    for item in dhdt:
        print(item)

    # Convert the binned data into colour-coded chart thing
    dhdt.reverse()
    dhdt = hm.main(dhdt)

    print("Binning complete.")
    print("\n")

    time.sleep(600)