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
    # Load up file into array. file is 1 minute bins.
    # print(k.INPUT_FILE)
    importarray = am.CreateRawArray(k.INPUT_FILE)

    # remove the first line which may contain text header
    importarray.pop(0)

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
    binner.SaveRawArray(dhdt, "output.csv")

    # Convert the binned data into colour-coded chart thing
    dhdt.reverse()
    dhdt = hm.main(dhdt)

    print("Binning complete.")
    print("\n")

    time.sleep(600)