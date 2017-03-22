import constants as k
import ArrayManager as am
import time
import binlibrary as binner
import heatmapconverter as hm
import urllib.request as webreader

# ###############################################
# Main Parts STarts Here
# ###############################################
url = "http://Dunedinaurora.nz/Service24CSV.php"
while True:
    importarray = []
    response = webreader.urlopen(url)
    for item in response:
        logData = str(item, 'ascii').strip()
        logData = logData.split(",")
        dp = logData[0] + "," + logData[1]
        importarray.append(dp)

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

    time.sleep(600)