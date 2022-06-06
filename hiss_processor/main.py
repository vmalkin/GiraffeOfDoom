from statistics import mean
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

        self.utc = self.dd[0]
        self.data = self.dd[1:]

        self.hz_data = [0, 0, 0, 0, 0, 0, 0]

        # Add data if exists to data array
        if self.utc != 'YYYY-MM-DD hh:mm:ss':
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
            pass


    # # Calculate dh/dt and populate the diffs array in each datapoint
    # for i in range(1, len(datapoint_array)):
    #     for j in range(0, 7):
    #         datapoint_array[i].diff_data[j] = float(datapoint_array[i].hz_data[j]) - float(datapoint_array[i - 1].hz_data[j])

    # Save out averaged readings
    # 6 readings a minute
    interval = 6 * 60

    final = [[],[],[],[],[],[],[]]
    t = [[],[],[],[],[],[],[]]

    for i in range(0, len(datapoint_array)):
        for j in range(0, 7):
            dp = float(datapoint_array[i].hz_data[j])
            t[j].append(dp)

        if i % interval == 0:
            # print(t)
            dt = datapoint_array[i].utc
            for j in range(0, 7):
                dd = round(mean(t[j]), 5)
                dp = str(dt) + "," + str(dd)
                final[j].append(dp)
            t = [[], [], [], [], [], [], []]

    for i in range(0, len(final)):
        filename = frequencies[i] + ".csv"
        with open(filename, "w") as f:
            for line in final[i]:
                f.write(line + "\n")
            f.close()





