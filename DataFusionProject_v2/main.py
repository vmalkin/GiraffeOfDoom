import Station
from datetime import datetime
import time
import os

# create the stations for the magnetometers
stationlist = []
print("Creating magentometer stations")
null_value = ""
try:
    station3 = Station.Station("Ruru - Standard", "/home/vmalkin/Magnetometer/publish/Dalmore_Prime.1minbins.csv")
    # station3 = Station.Station("Ruru - Standard", "Dalmore_Prime.1minbins.csv")
    stationlist.append(station3)
    print("Station Created!")
except:
    print("Unable to create station!")
try:
    station2 = Station.Station("Ruru - Rapid Run", "/home/vmalkin/Magnetometer/RuruRapid/graphing/RuruRapid.1minbins.csv")
    # station2 = Station.Station("Ruru - Rapid Run", "RuruRapid.1minbins.csv")
    stationlist.append(station2)
    print("Station Created!")
except:
    print("Unable to create station!")
try:
    station1 = Station.Station("Corstorphine", "/home/vmcdonal/vicbins/Corstorphine01.1minbins.csv")
    print("Station Created!")
    stationlist.append(station1)
except:
    print("Unable to create station!")


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
    while True:
        # force a refresh of station data from CSV files
        for magstations in stationlist:
            magstations.refresh_stationdata()

        aggregated_data = []
        nowtime = int(time.time())

        print("Creating array for aggregation...")
        # determin the one min UTC timestamps for the last 24 hours. Create an array to hold these
        for i in range(0, 1440):
            nowtime = nowtime - 60
            # Convert the unix date to UTC time
            utctime = datetime.utcfromtimestamp(nowtime).strftime("%Y-%m-%d %H:%M")
            dp = DisplayDatapoint(utctime)
            aggregated_data.append(dp)

        # the timestamps will be back-to-front, reverse the aggregated data so they age in the correct sequence
        aggregated_data.reverse()

        print("Aggregating data for station 1")
        for item in aggregated_data:
            for datapoint in station1.datalist_normalised:
                if item.utctime == datapoint.date:
                    item.data_1 = datapoint.data

        print("Aggregating data for station 2")
        for item in aggregated_data:
            for datapoint in station2.datalist_normalised:
                if item.utctime == datapoint.date:
                    item.data_2 = datapoint.data

        print("Aggregating data for station 3")
        for item in aggregated_data:
            for datapoint in station3.datalist_normalised:
                if item.utctime == datapoint.date:
                    item.data_3 = datapoint.data

        # Add a header to the CSV data
        header = DisplayDatapoint("datetime")
        header.data_1 = station1.station_name
        header.data_2 = station2.station_name
        header.data_3 = station3.station_name
        aggregated_data.reverse()
        aggregated_data.append(header)
        aggregated_data.reverse()

        print("Saving Merged Data")
        filename = "/home/vmalkin/Magnetometer/publish/merged.csv"
        # filename = "merged.csv"
        os.remove(filename)
        try:
            with open(filename, 'a') as w:
                for items in aggregated_data:
                    w.write(items.print_values() + '\n')
        except:
            pass
        print("Done!")

        time.sleep(300)
