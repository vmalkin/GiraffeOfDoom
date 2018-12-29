import datetime
import os
import shutil
spectrumlab_data = "z://temp//test.csv"
frankencoil_data = "working.csv"

if __name__ == "__main__":
    # get current date-time.

    if os.path.isfile(spectrumlab_data):
        shutil.copyfile(spectrumlab_data, frankencoil_data)
        UTC_date = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        frankenCoil_current_datafile = "FrankenCoil_" + UTC_date + ".csv"

        storage_array = []
        storage_array.append("UTC Date/Time, Average Noise, Average Amplitude")

        with open(frankencoil_data, "r") as f:
            for line in f:
                line = line.strip()
                datasplit = line.split(" ")
                if datasplit[0] == UTC_date:
                    storage_array.append(line)
        f.close()

        with open(frankenCoil_current_datafile, "a") as f:
            for line in storage_array:
                f.write(line + "\n")
        f.close()
            
    else:
        print("FrankenCoil data is not accessible - Aborting!")


