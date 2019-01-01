import datetime
import os
import shutil
spectrumlab_data = "z://temp//test.csv"
frankencoil_data = "working.csv"
running_avg_window = 20
null_value = ""
reading_threshold = -115

# raw data should have the format "utcdate, avg noise, avg reading"


class Datapoint:
    def __init__(self, datetime, avg_noise, avg_reading):
        self.datetime = datetime
        self.noise = avg_noise
        self.reading = avg_reading
        self.reading_db = null_value
        self.running_average = null_value
        
    def print_labels(self):
        labelstring = "UTC Date/Time,Magnetic noise,Reading (dB),Average Amplitude"
        # labelstring = "UTC Date/Time,Magnetic noise,Reading (dB),deblipped, Average Amplitude"
        return labelstring
        
    def print_values(self):
        returnstring = str(self.datetime) + "," + str(self.noise) + "," + str(self.reading) + "," + str(self.running_average)
        # returnstring = str(self.datetime) + "," + str(self.noise) + "," + str(self.reading) + "," + str(self.reading_db) + "," + str(self.running_average)
        return returnstring


def deblip_readings(object_list):
    for i in range(0, len(object_list)):
        if float(object_list[i].reading) < float(reading_threshold):
            object_list[i].reading_db = object_list[i].reading


# uses deblipped readings
def running_average(object_list):
    half_window = int(round((running_avg_window / 2), 0))
    
    for i in range(half_window, len(object_list) - half_window):
        avg_value = float(0)
        divider = 0
        for j in range(half_window * -1, half_window):
            if object_list[i+j].reading_db != null_value:
                avg_value = avg_value + float(object_list[i+j].reading_db)
                divider = divider + 1

        avg_value = round((avg_value / divider), 4)
        object_list[i].running_average = avg_value



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
                    ds = line.split(",")
                    dp = Datapoint(ds[0], ds[1], ds[2])
                    storage_array.append(dp)
        f.close()
        
        # perform the running average and update the datapoint property
        deblip_readings(storage_array)
        if len(storage_array) > running_avg_window:
            running_average(storage_array)
        
        # create the daily CSV logfile
        with open(frankenCoil_current_datafile, "w") as f:
            f.write(storage_array[0].print_labels() + "\n")

            for dp in storage_array:
                f.write(dp.print_values() + "\n")
        f.close()
        
        # this is the copy that gets updated to the website
        shutil.copyfile(frankenCoil_current_datafile, "frankencoil.csv")
            
    else:
        print("FrankenCoil data is not accessible - Aborting!")


