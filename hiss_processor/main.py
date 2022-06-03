from statistics import mean

# YYYY-MM-DD hh:mm:ss,125hz,240hz,410hz,760hz,1800hz,4300hz,9000hz
# 2022-01-15 04:13:34,36.243,33.482,23.342,21.961,17.429,3.902,-3.328
hissfile = "hiss.csv"
sightingsfile = "sightings.csv"

class DataPoint:
    def __init__(self, data_csv):
        self.sightings = 0
        self.d = data_csv.strip()
        self.dd = self.d.split(",")
        self.utc = self.dd[0]

        self.hz_data = []
        self.diff_data = []

        # prepopulate data array with zeros
        for i in range(0, 7):
            self.hz_data.append(0)

        # Add data if exists to data array
        if self.utc != 'YYYY-MM-DD hh:mm:ss':
            for i in range(0, 7):
                self.hz_data.append(self.dd[i])

        # prepopulate diffs array with zeros
        for i in range(0, 7):
            self.diff_data.append(0)


datapoint_array = []
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open(hissfile, "r") as h:
        for line in h:
            dp = DataPoint(line)
            datapoint_array.append(dp)

    # Calculate dh/dt and populate the diffs array in each datapoint
    for i in range(1, len(datapoint_array)):
        for j in range(0, 7):
            datapoint_array[i].diff_data[j] = datapoint_array[i].diff_data[j] - datapoint_array[i - 1].diff_data[j]

    # 6 readings a minute
    interval = 6 * 60

    hz125 = []
    hz240 = []
    hz410 = []
    hz760 = []
    hz1800 = []
    hz4300 = []
    hz9000 = []

    t125 = []
    t240 = []
    t410 = []
    t760 = []
    t1800 = []
    t4300 = []
    t9000 = []

    for i in range(0, len(datapoint_array)):
        t125.append(datapoint_array[i].diff_data[0])
        t240.append(datapoint_array[i].diff_data[1])
        t410.append(datapoint_array[i].diff_data[2])
        t760.append(datapoint_array[i].diff_data[3])
        t1800.append(datapoint_array[i].diff_data[4])
        t4300.append(datapoint_array[i].diff_data[5])
        t9000.append(datapoint_array[i].diff_data[6])

        if i % 60 == 0:
            d125 = mean(t125)
            hz125.append([datapoint_array[i].utc, d125])

            d240 = mean(t240)
            hz240.append([datapoint_array[i].utc, d240])

            d410 = mean(t410)
            hz410.append([datapoint_array[i].utc, d410])

            d760 = mean(t760)
            hz760.append([datapoint_array[i].utc, d760])

            d1800 = mean(t1800)
            hz1800.append([datapoint_array[i].utc, d1800])

            d4300 = mean(t4300)
            hz4300.append([datapoint_array[i].utc, d4300])

            d9000 = mean(t9000)
            hz9000.append([datapoint_array[i].utc, d9000])

            t125 = []
            t240 = []
            t410 = []
            t760 = []
            t1800 = []
            t4300 = []
            t9000 = []


