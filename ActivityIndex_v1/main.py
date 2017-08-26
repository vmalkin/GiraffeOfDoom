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
        station1 = Station.Station("Dalmore Prime", "/home/vmalkin/Magnetometer/publish/Dalmore_Prime.1minbins.csv", "f1", '%Y-%m-%d %H:%M', 1)
    except:
        print("Unable to create Station")

    try:
        station2 = Station.Station("Dalmore Rapid Run No 01", "/home/vmalkin/Magnetometer/dalmoreR1/pyDataReader/graphing/Dalmore_Rapid_01.1minbins.csv", "f1", '%Y-%m-%d %H:%M', 1)
    except:
        print("Unable to create Station")

    try:
        station3 = Station.Station("Dalmore Rapid Run No 02", "/home/vmalkin/Magnetometer/dalmoreR2/pyDataReader/graphing/Dalmore_Rapid_02.1minbins.csv", "f1", '%Y-%m-%d %H:%M', 1)
    except:
        print("Unable to create Station")

    try:
        station4 = Station.Station("Corstorphine", "/home/vmcdonal/vicbins/Corstorphine01.1minbins.csv", "f1", '%Y-%m-%d %H:%M', 1)
    except:
        print("Unable to create Station")

    try:
        station5 = Station.Station("DunedinAurora.NZ", "http://Dunedinaurora.nz/Service24CSV.php", "w1", '"%Y-%m-%d %H:%M:%S"', 6)
    except:
        print("Unable to create Station")

    try:
       station6 = Station.Station("GOES-13 Satellite", "http://services.swpc.noaa.gov/text/goes-magnetometer-primary.txt", "w2", '%Y-%m-%d %H:%M', 1)
    except:
       print("Unable to create Station")

    # Add the stations to the station list
    stationlist = []
    try:
        stationlist.append(station1)
    except:
        print("Unable to add station to list")

    try:
        stationlist.append(station2)
    except:
        print("Unable to add station to list")

    try:
        stationlist.append(station3)
    except:
        print("Unable to add station to list")

    try:
        stationlist.append(station4)
    except:
        print("Unable to add station to list")

    try:
        stationlist.append(station5)
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

            # convert the absolute values to rates of change
            magstation.create_dadt()

            # create the one hour bins of dhdt
            print("Creating data bins...\n")
            magstation.do_bin_dh_dt()

            # We need to reduce our absolute values, to some relative value that accounts for historical
            # highs and lows. Find the Median? calculate the Standard Deviation??
            print("Normalising data...\n")
            magstation.normaliseDHDT()

            # create the combined output file
            combolist = []
            comboitem = "Station Name, NOW, 2hr, 3hr, 4hr, 5hr, 6hr, 7hr, 8hr, 9hr, 10hr, 11hr, 12hr, 13hr, 14hr, 15hr, 16hr, 17hr, 18hr, 19hr, 20hr, 21hr, 22hr, 23hr, 24hr"
            combolist.append(comboitem)

            for magstation in stationlist:
                comboitem = ""
                comboitem = comboitem + str(magstation.name)

                for measurement in magstation.bin_dadt:
                    comboitem = comboitem + "," + str(measurement)

                combolist.append(comboitem)

            SaveAsCSV(combolist)

        fintime = datetime.now()
        fintime = time.mktime(fintime.timetuple())

        totaltime = fintime - starttime
        nextfetch = fintime + sleeptime
        nextfetch = datetime.utcfromtimestamp(nextfetch).strftime('%Y-%m-%d %H:%M UTC')

        print("\nFINISHED! Processing time: " + str(totaltime) + " seconds. Next update at " + str(nextfetch))

        time.sleep(sleeptime)

