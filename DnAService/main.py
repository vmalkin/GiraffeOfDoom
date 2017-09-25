import time
from datetime import datetime
import Station

# setup dictionary of stations
# each item has the format ("name", "data_source", "source_type", readings_per_minute)
station_details = (
    ("GOES-13 Satellite", "http://services.swpc.noaa.gov/text/goes-magnetometer-secondary.txt", "w2", '%Y-%m-%d %H:%M', 1),
    ("Ruru Observatory Rapid Run No 01", "http://www.ruruobservatory.org.nz/dr01_1hr.csv", "w3", "%Y-%m-%d %H:%M:%S.%f", 30),
    ("DunedinAurora.NZ", "http://Dunedinaurora.nz/Service24CSV.php", "w1", '"%Y-%m-%d %H:%M:%S"', 6)
)

station_list = []

for item in station_details:
    new_station = Station.Station(item)
    station_list.append(new_station)

for mag_station in station_list:
    # load station PKL file.
    pass

if __name__ == "__main__":
    # while True:
    # calculate the processing time
        starttime = datetime.now()
        starttime = time.mktime(starttime.timetuple())
        # for each station.....
        for mag_station in station_list:
            mag_station.process_mag_station()


        # Create aggregate list of dF/dt
        # Create aggregate list of reconstructed magnetogram
        # save to CSV or JSON file

        finishtime = datetime.now()
        finishtime = time.mktime(finishtime.timetuple())

        elapsedtime = finishtime - starttime
        elapsedtime = float(elapsedtime / 60)
        print("\nElapsed time is " + str(elapsedtime) + " minutes.")
        # time.sleep(120)