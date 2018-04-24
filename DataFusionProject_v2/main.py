import Station
import logging
import datetime
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
        path = "/home/vmalkin/Magnetometer/publish/"
        # path = ""
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

    # create the entries for each station
    logging.info("Creating the instance of each station...")

    while True:
        # station1 = Station.Station("Dalmore Rapid No 1", "dr_01hr.csv")
        try:
            # station1 = Station.Station("Dalmore Prime", "/home/vmalkin/Magnetometer/publish/Dalmore_Prime.1minbins.csv")
            station1 = Station.Station("Dalmore Rapid No 1", "Dalmore_Rapid_01.1minbins.csv")
        except:
            print("Unable to create station1")

        try:
            # station2 = Station.Station("Dalmore Rapid No 1", "/home/vmalkin/Magnetometer/dalmoreR1/pyDataReader/graphing/Dalmore_Rapid_01.1minbins.csv")
            station2 = Station.Station("Dalmore Rapid No 2", "Dalmore_Rapid_02.1minbins.csv")
        except:
            print("Unable to create station2")

        # try:
        #     station3 = Station.Station("Dalmore Rapid No 2", "/home/vmalkin/Magnetometer/dalmoreR2/pyDataReader/graphing/Dalmore_Rapid_02.1minbins.csv")
        # except:
        #     print("Unable to create station3")
        #
        try:
            station4 = Station.Station("Corstorpine", "Corstorphine01.1minbins.csv")
        except:
            print("Unable to create station4")

        # we're only ever going to have a handful of stations here, so just manually append them
        logging.info("Creating the list of magnetometer stations")
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

