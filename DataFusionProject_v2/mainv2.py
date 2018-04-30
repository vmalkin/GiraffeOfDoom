import Station
from datetime import datetime
import time

# create the stations for the magnetometers
station1 = Station.Station("Rure No 1", "Dalmore_Prime.1minbins.csv")
station2 = Station.Station("Ruru Rapid No 2", "RuruRapid.1minbins.csv")
station3 = Station.Station("Corstorpine", "Corstorphine01.1minbins.csv")

# create the array of stations
stationlist = []
stationlist.append(station1)
stationlist.append(station2)
stationlist.append(station3)


if __name__ == "__main__":
    null_value = ""
    # determin the one min UTC timestamps for the last 24 hours. Create an array to hold these
    for i in range(0, 1440):
        # Convert the unix date to UTC time
        utctime = datetime.fromtimestamp(int(unixdate)).strftime("%Y-%m-%d %H:%M")
    # Populate each timestamp in the array from each station in sequence, filling in a NULL if there is no entry
    pass