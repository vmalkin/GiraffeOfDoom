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
    # print(k.FILE_BINNED_MINS)
    importarray = am.CreateRawArray(k.FILE_BINNED_MINS)

    # remove the first line which may contain text header
    importarray.pop(0)

    # create the bins for dh/dt
    dhdt = importarray
    dhdt = binner.utc2unix(dhdt)
    dhdt = binner.bin_dh_dt(dhdt)

    # Process the array and return the coded verson that will display as colour or whatever
    dhdt = hm.main(dhdt)
    dhdt.reverse()

    binner.SaveRawArray(dhdt)
    print("Binning complete.")

    for item in dhdt:
        print(item)

    print("\n")

    time.sleep(600)