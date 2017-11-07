import time
from datetime import datetime
import Station


# #################################################################################
# Save the binned data as CSV file
# #################################################################################
def SaveAsCSV(datalist):
    # export array to array-save file
    try:
        with open("combo.csv", 'w') as w:
            for item in datalist:
                w.write(item + '\n')
    except IOError:
        print("WARNING: There was a problem saving binned CSV data")


if __name__ == '__main__':
    stationlist = []
    try:
        station1 = Station.Station("Dalmore Prime", "http://www.ruruobservatory.org.nz/Dalmore_Prime.1minbins.csv", "w1", '%Y-%m-%d %H:%M', 1)
        # station1 = Station.Station("Dalmore Prime", "Dalmore_Prime.1minbins.csv", "f1", '%Y-%m-%d %H:%M', 1)
    except:
        print("Unable to create Station")

    try:
       station6 = Station.Station("GOES-13 Satellite", "http://services.swpc.noaa.gov/text/goes-magnetometer-secondary.txt", "w2", '%Y-%m-%d %H:%M', 1)
    except:
       print("Unable to create Station")

    # Add the stations to the station list
    stationlist = []
    try:
        stationlist.append(station1)
    except:
        print("Unable to add station to list")

    try:
        stationlist.append(station6)
    except:
        print("Unable to add station to list")


    while True:
        sleeptime = 900
        starttime = datetime.now()
        starttime = time.mktime(starttime.timetuple())

        for magstation in stationlist:
            print("\n")
            # grab newest data
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            print("Getting new data...\n")
            magstation.get_data()

            # convert new data time to UNIX
            print("Converting to UNIX time...\n")
            magstation.utc2unix()

            # get the latest timestamp from the saved_data. ONly add new data
            # to saved_data that is after thhis latest timestamp
            print("Appending new data...\n")
            magstation.append_new_data()
            print("Pruning OLD data...\n")
            magstation.prune_saved_data()

            # # save out the station data as a CSV file.
            name = magstation.name + ".absl"
            magstation.SaveAsCSV(name)

            # finally, save the station saved_data array to file.
            print("Save data to file...\n")
            magstation.savepickle()

        fintime = datetime.now()
        fintime = time.mktime(fintime.timetuple())

        totaltime = fintime - starttime
        nextfetch = fintime + sleeptime
        nextfetch = datetime.utcfromtimestamp(nextfetch).strftime('%Y-%m-%d %H:%M UTC')

        print("\nFINISHED! Processing time: " + str(totaltime) + " seconds. Next update at " + str(nextfetch))

        time.sleep(sleeptime)

