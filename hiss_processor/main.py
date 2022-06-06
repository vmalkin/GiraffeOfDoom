import math
from statistics import mean, stdev
import standard_stuff

# YYYY-MM-DD hh:mm:ss,125hz,240hz,410hz,760hz,1800hz,4300hz,9000hz
# 2022-01-15 04:13:34,36.243,33.482,23.342,21.961,17.429,3.902,-3.328
hissfile = "hiss.csv"
sightingsfile = "sightings.csv"
frequencies = ["125hz","240hz","410hz","760hz","1800hz","4300hz","9000hz"]

class DataPoint:
    def __init__(self, data_csv):
        self.sightings = 0
        self.d = data_csv.strip()
        self.dd = self.d.split(",")

        self.utc = 0
        self.data = self.dd[1:]

        self.hz_data = [0, 0, 0, 0, 0, 0, 0]

        # Add data if exists to data array
        if self.dd[0] != 'YYYY-MM-DD hh:mm:ss':
            self.utc = standard_stuff.utc2posix(self.dd[0], "%Y-%m-%d %H:%M:%S")
            for i in range(0, 7):
                self.hz_data[i] = self.data[i]



datapoint_array = []
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open(hissfile, "r") as h:
        for line in h:
            dp = DataPoint(line)
            datapoint_array.append(dp)

    # Add sightings to datapoints
    with open(sightingsfile, "r") as s:
        for line in s:
            l = line.strip()
            dt = standard_stuff.utc2posix(l, "%d-%m-%Y")
            for item in datapoint_array:
                dx = (item.utc - dt) ** 2
                dx = math.sqrt(dx)
                if dx <= 43200:
                    item.sightings = 1

    interval = 6 * 60

    final = [[],[],[],[],[],[],[]]
    statsvalues = [[],[],[],[],[],[],[]]
    t = [[],[],[],[],[],[],[]]
    sighting = 0

    for i in range(0, len(datapoint_array)):
        sighting = sighting + datapoint_array[i].sightings
        for j in range(0, 7):
            dp = float(datapoint_array[i].hz_data[j])
            t[j].append(dp)

        if i % interval == 0:
            dt = datapoint_array[i].utc
            dt = standard_stuff.posix2utc(dt, "%Y-%m-%d %H:%M")
            ds = 0
            if sighting > 0:
                ds = 1
            for j in range(0, 7):
                dd = round(mean(t[j]), 5)
                dp = str(dt) + "," + str(dd) + "," + str(ds)
                statsvalues[j].append(dd)
                final[j].append(dp)
            t = [[], [], [], [], [], [], []]
            sighting = 0

    # Save to file
    for i in range(0, len(final)):
        # generate stats
        mm = round(mean(statsvalues[i]), 4)
        sd = stdev(statsvalues[i])
        sd1 = round((mm + sd * 1), 4)
        sd2 = round((mm + sd * 2), 4)
        sd3 = round((mm + sd * 3), 4)
        sd4 = round((mm + sd * 4), 4)
        sd5 = round((mm + sd * 5), 4)
        statsline = "," + str(mm) + "," + str(sd1) + "," + str(sd2) + "," + str(sd3) + "," + str(sd4) + "," + str(sd5)

        filename = frequencies[i] + ".csv"
        with open(filename, "w") as f:
            f.write("UTC, value, aurora, mean, sd1, sd2, sd3, sd4, sd5\n")
            for line in final[i]:
                f.write(line + statsline + "\n")
            f.close()





