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
