from datetime import datetime, timedelta
import os
import shutil
import math
spectrumlab_data = "c://temp//test.csv"
frankencoil_data = "working.csv"
running_avg_window = 20
null_value = ""
reading_threshold = -115
noise_threshold = -108.1
mag_noise_dhdt = 0.15
__version__ = "0.2"

# raw data should have the format "utcdate, avg noise, avg reading"


class Datapoint:
    def __init__(self, datetime, avg_noise, avg_reading):
        self.datetime = datetime
        self.noise = avg_noise
        self.reading = avg_reading
        self.reading_db = null_value
        self.noise_db = null_value
        self.average_reading = null_value
        self.average_noise = null_value
        self.dndt = 0
        
    def print_labels(self):
        labelstring = "UTC Date/Time,Magnetic noise, Induced Signal(dB),Average Magnetic Noise,Average Induced Signal"
        return labelstring
        
    def print_values(self):
        returnstring = str(self.datetime) + "," + str(self.noise) + "," + str(self.reading) + "," + str(self.average_noise) + "," + str(self.average_reading)
        return returnstring


def deblip_readings(object_list):
    for i in range(0, len(object_list)):
        if float(object_list[i].reading) < float(reading_threshold):
            object_list[i].reading_db = object_list[i].reading

def deblip_noise(object_list):
    for i in range(0, len(object_list)):
        if float(object_list[i].noise) < float(noise_threshold):
            object_list[i].noise_db = object_list[i].noise

def deblip_magnetic_noise(object_list):
    for i in range (1, len(object_list)):
        dndt = object_list[i].noise - object_list[i-1].noise
        if math.sqrt(dndt**2) > mag_noise_dhdt:
            object_list[i].dndt = dndt
            
    object_list[0].average_noise = object_list[0].noise
    for i in range(1, len(object_list)):
        object_list[i].average_noise = object_list[i-1].average_noise + object_list[i].dndt
        

# uses deblipped readings
def average_reading(object_list):
    half_window = int(round((running_avg_window / 2), 0))
    
    for i in range(half_window, len(object_list) - half_window):
        avg_value = float(0)
        divider = 0
        for j in range(half_window * -1, half_window):
            if object_list[i+j].reading_db != null_value:
                avg_value = avg_value + float(object_list[i+j].reading_db)
                divider = divider + 1

        if divider > 0:
            avg_value = round((avg_value / divider), 4)
            object_list[i].average_reading = avg_value


def average_noise(object_list):
    half_window = int(round((running_avg_window / 2), 0))

    for i in range(half_window, len(object_list) - half_window):
        avg_value = float(0)
        divider = 0
        for j in range(half_window * -1, half_window):
            if object_list[i + j].noise_db != null_value:
                avg_value = avg_value + float(object_list[i + j].noise_db)
                divider = divider + 1

        if divider > 0:
            avg_value = round((avg_value / divider), 4)
            object_list[i].average_noise = avg_value

if __name__ == "__main__":
    print("FrankenCoil Parser Version " + __version__ + "\n")
    if os.path.isfile(spectrumlab_data):
        shutil.copyfile(spectrumlab_data, frankencoil_data)
        UTC_date_1 = datetime.utcnow().strftime("%Y-%m-%d")
        UTC_date_0 = datetime.utcnow() - timedelta(days=1)
        UTC_date_0 = UTC_date_0.strftime("%Y-%m-%d")
        frankenCoil_current_datafile = "FrankenCoil_" + UTC_date_1 + ".csv"

        # Parse out the current daily data from Spectrum Lab's generic csv file
        storage_array = []
        with open(frankencoil_data, "r") as f:
            for line in f:
                line = line.strip()
                datasplit = line.split(" ")
                if (datasplit[0] == UTC_date_0) or (datasplit[0] == UTC_date_1):
                    ds = line.split(",")
                    dp = Datapoint(ds[0], ds[1], ds[2])
                    storage_array.append(dp)
        f.close()
        
        # perform the running average and update the datapoint property
        deblip_readings(storage_array)
        deblip_noise(storage_array)
        if len(storage_array) > running_avg_window:
            average_reading(storage_array)
            average_noise(storage_array)
        
        # create the daily CSV logfile
        with open(frankenCoil_current_datafile, "w") as f:
            f.write(storage_array[0].print_labels() + "\n")

            for dp in storage_array:
                f.write(dp.print_values() + "\n")
        f.close()
        
        # this is the copy that gets updated to the website
        shutil.copyfile(frankenCoil_current_datafile, "frankencoil.csv")
        print("Finished Parsing")
            
    else:
        print("FrankenCoil data is not accessible - Aborting!")


