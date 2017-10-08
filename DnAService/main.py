import time
from datetime import datetime
import Station
import os

# setup dictionary of stations
# each item has the format ("name", "data_source", "source_type", " datetime regex", readings_per_minute)
# station_details = (
#     ("GOES-13 Satellite", "http://services.swpc.noaa.gov/text/goes-magnetometer-secondary.txt", "w2", '%Y-%m-%d %H:%M', 1),
#     ("Ruru Observatory", "http://www.ruruobservatory.org.nz/dr01_1hr.csv", "w3", "%Y-%m-%d %H:%M:%S.%f", 30),
#     ("DunedinAurora.NZ", "http://Dunedinaurora.nz/Service24CSV.php", "w1", '"%Y-%m-%d %H:%M:%S"', 6)
# )
station_details = (("Ruru Observatory", "http://www.ruruobservatory.org.nz/dr01_1hr.csv", "w3", "%Y-%m-%d %H:%M:%S.%f", 30),("GOES-13 Satellite", "http://services.swpc.noaa.gov/text/goes-magnetometer-secondary.txt", "w2", '%Y-%m-%d %H:%M', 1))

# create the list of magnetometer stations
station_list = []
for item in station_details:
    new_station = Station.Station(item)
    station_list.append(new_station)


# ##################################################
# F U N C T I O N S
# ##################################################

def create_one_minute_bin_values():
    # what is the current datetime? create a UNix timetuple
    nowtime = datetime.utcnow()
    nowtime = time.mktime(nowtime.timetuple())

    # create the list of time values for the past 24 hours
    bins = []
    for i in range(0, 1441):  # one min bins
        bins.append(nowtime)
        nowtime = nowtime - 60
    # reverse so the most recent data is last
    bins.reverse()
    return bins

# take in a datalist and two time values, output an average value for whatever data falls in-between the time range
def create_binned_data(prev_time, next_time, datalist):
    # data list has the format: unix_datetime, data
    tempstore = 0
    counter = 0
    for i in range(0, len(datalist)):
        datasplit = datalist[i].split(",")
        date_to_check = float(datasplit[0])
        data_to_add = datasplit[1]

        if date_to_check >= prev_time and date_to_check < next_time:
            tempstore = tempstore + float(data_to_add)
            counter += 1

    if tempstore == 0:
        bin_value = 0
    else:
        bin_value = float(tempstore / counter)

    return bin_value

def create_aggregated_magnetometer_values(stationlist):
    time_bins = create_one_minute_bin_values()

    # For each station, we need to check off what values it has that fall into our time bins, calculate the
    # average of that and append it to the final output file that will be used by the website.
    finaloutput = []
    for i in range(1, len(time_bins)):
        timeprev = time_bins[i-1]
        timenext = time_bins[i]
        aggregated_readings = ""

        for mag_station in stationlist:
            returnvalue = create_binned_data(timeprev, timenext, mag_station.stationdata)

        aggregated_readings = aggregated_readings + "," + str(returnvalue)

        finaldata = str(time_bins[i]) + "," + aggregated_readings
        finaloutput.append(finaldata)

    # return the final, aggregated, binned outputs
    return finaloutput


# ##################################################
# Save out CSV data
# ##################################################
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
    dateformat = "%Y-%m-%d %H:%M:%S"

    # Convert the date string to the format of: 2016-10-10 00:00:26.19
    returnarray = []

    for j in range(1, len(arraylist)):
        datasplit = arraylist[j].split(",")
        unixdate = datasplit[0]
        unixdate = unixdate.split(".")
        unixdate = unixdate[0]

        datavalues = ""
        for i in range(1, len(datasplit)):
            datavalues = "," + datasplit[i]

        # Convert the UNix timestamp, into a UTC string
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
    aggregated_data = create_aggregated_magnetometer_values(station_list)
    # convert the timesampts to UTC for display on the website
    aggregated_data = unix_to_utc(aggregated_data)

    # save to CSV or JSON OUTPUT file
    save_csv(aggregated_data, "aggregate.csv")

    # Calculate the elapsed processing time and display the result to the console...
    finishtime = datetime.now()
    finishtime = time.mktime(finishtime.timetuple())
    elapsedtime = finishtime - starttime
    # elapsedtime = float(elapsedtime / 60)
    print("\nElapsed time is " + str(elapsedtime) + " seconds")

        # time.sleep(2 * 60)