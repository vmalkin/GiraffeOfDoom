import datetime
import os
import shutil
import math
spectrumlab_data = "z://temp//test.csv"
frankencoil_data = "working.csv"
running_avg_window = 20

# raw data should have the format "utcdate, avg noise, avg reading"

class Datapoint:
    def __init__(self, datetime, avg_noise, avg_reading):
        self.datetime = datetime
        self.noise = avg_noise
        self.reading = avg_reading
        self.running_average = 0
        
    def print_labels(self):
        labelstring = "UTC Date/Time,Magnetic noise,Reading (dB),Average"
        return labelstring
        
    def print_values(self):
        returnstring = self.datetime + "," + self.noise + "," + self.reading + "," + self.running_average
        return returnstring

def running_average(object_list):
    object_list.reverse()
    
    for i in range(0, len(object_list) - running_avg_window):
        avg_value = 0
        for j in range(0, running_avg_window):
            avg_value = avg_value + float(object_list[i+j].reading)
        
        avg_value = avg_value / running_avg_window
        object_list[i].running_average = avg_value
            
    object_list.reverse()
    
    return object_list

if __name__ == "__main__":
    if os.path.isfile(spectrumlab_data):
        shutil.copyfile(spectrumlab_data, frankencoil_data)
        UTC_date = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        frankenCoil_current_datafile = "FrankenCoil_" + UTC_date + ".csv"

        # Parse out the current daily data from Spectrum Lab's generic csv file
        storage_array = []
        with open(frankencoil_data, "r") as f:
            for line in f:
                line = line.strip()
                datasplit = line.split(" ")
                if datasplit[0] == UTC_date:
                    dp = Datapoint(datasplit[0], datasplit[1], datasplit[2])
                    storage_array.append(dp)
        f.close()
        
        # perform the running average and update the datapoint property
        if len(storage_array) > running_avg_window:
            storage_array = running_average(storage_array)
        
        # create the daily CSV logfile
        with open(frankenCoil_current_datafile, "w") as f:
            f.write(dp.print_labels + "\n")
            for dp in storage_array:
                f.write(dp.print_values() + "\n")
        f.close()
        
        # this is the copy that gets updated to the website
        shutil.copyfile(frankenCoil_current_datafile, "frankencoil.csv")
            
    else:
        print("FrankenCoil data is not accessible - Aborting!")


