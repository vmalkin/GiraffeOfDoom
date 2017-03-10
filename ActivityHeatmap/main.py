import constants as k
import ArrayManager as am
import time
import binlibrary as binner

# ###############################################
# Main Parts STarts Here
# ###############################################

while True:
    importarray = []
    # Load up file into array
    # print(k.FILE_BINNED_MINS)
    importarray = am.CreateRawArray(k.FILE_BINNED_MINS)

<<<<<<< HEAD
    except:
        print("The Binning Program has failed for some general reason")
=======
    # remove the first line which may contain text header
    importarray.pop(0)

    # create the bins for dh/dt
    importarray = binner.utc2unix(importarray)
    importarray = binner.bin_dh_dt(importarray)

    binner.SaveRawArray(importarray)
    print("Binning complete.")

    importarray.sort()

    print(importarray[int(len(importarray) / 2)])
>>>>>>> origin/master

    time.sleep(600)