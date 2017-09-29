import time
from datetime import datetime
import Station
import os

# setup dictionary of stations
# each item has the format ("name", "data_source", "source_type", " datetime regex", readings_per_minute)
station_details = (
    ("GOES-13 Satellite", "http://services.swpc.noaa.gov/text/goes-magnetometer-secondary.txt", "w2", '%Y-%m-%d %H:%M', 1),
    ("Ruru Observatory Rapid-run magnetometer", "http://www.ruruobservatory.org.nz/dr01_1hr.csv", "w3", "%Y-%m-%d %H:%M:%S.%f", 30),
    ("DunedinAurora.NZ", "http://Dunedinaurora.nz/Service24CSV.php", "w1", '"%Y-%m-%d %H:%M:%S"', 6)
)

station_list = []

for item in station_details:
    new_station = Station.Station(item)
    station_list.append(new_station)

# Create the one mininte aggregated bin file thing!
def oneminbin(stationlist):
    nowtime = datetime.now()
    nowtime = time.mktime(nowtime.timetuple())

    time_bins = []
    label_list = []

    # create the list of time values for the past 24 hours
    for i in range(0, 1441): # one min bins
        time_bins.append(nowtime)
        nowtime = nowtime - 60
    # reverse so the most recent data is last
    time_bins.reverse()

    finaloutput = []

    for i in range(1,len(time_bins)):
        finaloutput_data = time_bins[i]
        for mag_station in station_list:
            avg_value = 0
            counter = 0

            for item in mag_station.stationdata:
                datasplit = item.split(",")
                if float(datasplit[0]) >= time_bins[i-1] and float(datasplit[0]) < time_bins[i]:
                    avg_value = float(avg_value) + float(datasplit[1])
                    counter = counter + 1

            if counter > 0:
                avg_value = float(avg_value / counter)
            else:
                avg_value = 0
            finaloutput_data = str(finaloutput_data) + "," + str(avg_value)


        finaloutput.append(finaloutput_data)

    finaloutput.reverse()
    names = "UTC Datetime"
    for mag_station in station_list:
        names = names + "," + mag_station.name
    finaloutput.append(names)
    finaloutput.reverse()

    return finaloutput

def save_csv(arraydata, savefile):
    try:
        os.remove(savefile)
    except:
        print("Error deleting old file")

    for line in arraydata:
        try:
            with open(savefile, 'a') as f:
                f.write(line + "\n")

        except IOError:
            print("WARNING: There was a problem accessing heatmap file")

# ##################################################
# Convert timestamps in array to UTC time
# ##################################################
def unix_to_utc(arraylist):
    print("Converting time to UTC time...")
    # set date time format for strptime()
    dateformat = "%Y-%m-%d %H:%M:%S.%f"

    # Convert the date string to the format of: 2016-10-10 00:00:26.19
    returnarray = []

    for j in range(1,len(arraylist)):
        datasplit = arraylist[j].split(",")
        unixdate = datasplit[0]
        unixdate = unixdate.split(".")
        unixdate = unixdate[0]

        print(len(datasplit))

        datavalues = ""
        for i in range(1, len(datasplit)):
            datavalues = "," + datasplit[i]


        # Convert the UNix timestamp, inot a UTC string
        utcdate = datetime.fromtimestamp(int(str(unixdate)))

        # Create the dataline to be appended
        dataline = str(utcdate) + datavalues
        returnarray.append(dataline)

    return returnarray

# ############################################
# Main method starrts here
# ############################################
if __name__ == "__main__":
    # while True:
    # calculate the processing time
    starttime = datetime.now()
    starttime = time.mktime(starttime.timetuple())
    # for each station.....
    for mag_station in station_list:
        mag_station.process_mag_station()

    # Create aggregate list of dF/dt
    # create the combined output file
    aggregated_data = []
    aggregated_data = oneminbin(station_list)
    aggregated_data = unix_to_utc(aggregated_data)

    # save to CSV or JSON file
    save_csv(aggregated_data, "aggregate.csv")

    finishtime = datetime.now()
    finishtime = time.mktime(finishtime.timetuple())

    elapsedtime = finishtime - starttime
    elapsedtime = float(elapsedtime / 60)
    print("\nElapsed time is " + str(elapsedtime) + " minutes.")

        # time.sleep(121)