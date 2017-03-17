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
    dhdt = binner.utc2unix(dhdt)
    dhdt = binner.bin_dh_dt(dhdt)

    # for item in dhdt:
    #     print(item)

    # Process the array and return the coded verson that will display as colour or whatever
    dhdt.reverse()
    dhdt = hm.main(dhdt)

    print("Binning complete.")



    print("\n")

    time.sleep(600)