import Station
import logging
import datetime
import mgr_binner
import time


# ####################################################################################
# converts the UTC timestamp to unix datatime. returns converted array.
# ####################################################################################
def unix2utc(unixdate):
    utctime = datetime.datetime.fromtimestamp(int(unixdate)).strftime('%Y-%m-%d %H:%M:%S')
    return utctime

# #################################################################################
# Save the binned datadata as CSV file
# #################################################################################
def SaveAsCSV(datalist):
    # export array to array-save file
    try:
        # path = "/home/vmalkin/Magnetometer/publish/"
        path = ""
        with open(path + "merged.csv", 'w') as w:
            for item in datalist:
                w.write(item + '\n')
    except IOError:
        print("WARNING: There was a problem saving binned CSV datadata")

if __name__ == "__main__":
    # Setup error/bug logging
    # logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=logging.DEBUG)
    logging.basicConfig(filename="errors.log", format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info("Created error log for this session")

    binner = mgr_binner.Binner(array, 86400, 60, 1)
    binner.
    station1 = Station.Station("Rure No 1", "Dalmore_Prime.1minbins.csv")
    station2 = Station.Station("Ruru Rapid No 2", "RuruRapid.1minbins.csv")
    station3 = Station.Station("Corstorpine", "Corstorphine01.1minbins.csv")

    # we're only ever going to have a handful of stations here, so just manually append them
    logging.info("Creating the list of magnetometer stations")
    stationlist = []
    stationlist.append(station1)
    stationlist.append(station2)
    stationlist.append(station3)

    # load up CSV data for each station
    for mag_station in stationlist:
        mag_station.load_csv()
        mag_station.save_csv()
