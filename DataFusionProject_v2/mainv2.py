import Station
from datetime import datetime
import time

# create the stations for the magnetometers
null_value = ""
station1 = Station.Station("Rure No 1", "Dalmore_Prime.1minbins.csv")
station2 = Station.Station("Ruru Rapid No 2", "RuruRapid.1minbins.csv")
station3 = Station.Station("Corstorpine", "Corstorphine01.1minbins.csv")

# create the array of stations
stationlist = []
stationlist.append(station1)
stationlist.append(station2)
stationlist.append(station3)

class DisplayDatapoint():
    def __init__(self, utctime):
        self.utctime = utctime
        self.data_1 = null_value
        self.data_2 = null_value
        self.data_3 = null_value

    def print_values(self):
        returnstring = str(self.utctime) + "," + str(self.data_1) + "," + str(self.data_2) + "," + str(self.data_3)
        return returnstring

if __name__ == "__main__":
    aggregated_data = []
    nowtime = int(time.time())

    # determin the one min UTC timestamps for the last 24 hours. Create an array to hold these
    for i in range(0, 1440):
        nowtime = nowtime - 60
        # Convert the unix date to UTC time
        utctime = datetime.fromtimestamp(nowtime).strftime("%Y-%m-%d %H:%M")
        dp = DisplayDatapoint(utctime)
        aggregated_data.append(dp)

    # the timestamps will be back-to-front, reverse the aggregated data so they age in the correct sequence
    aggregated_data.reverse()



    for item in aggregated_data:
        print(item.print_values())
