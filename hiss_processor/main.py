# YYYY-MM-DD hh:mm:ss,125hz,240hz,410hz,760hz,1800hz,4300hz,9000hz
# 2022-01-15 04:13:34,36.243,33.482,23.342,21.961,17.429,3.902,-3.328
hissfile = "hiss.csv"

class DataPoint:
    def __init__(self, data_csv):
        self.d = data_csv.strip()
        self.dd = self.d.split(",")
        self.utc = self.dd[0]
        self.hz125 = self.dd[1]
        self.hz240 = self.dd[2]
        self.hz410 = self.dd[3]
        self.hz760 = self.dd[4]
        self.hz1800 = self.dd[5]
        self.hz4300 = self.dd[6]
        self.hz9000 = self.dd[7]

        self.diff125 = 0
        self.diff240 = 0
        self.diff410 = 0
        self.diff760 = 0
        self.diff1800 = 0
        self.diff4300 = 0
        self.diff9000 = 0


datapoint_array = []
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open(hissfile, "r") as h:
        for line in h:
            dp = DataPoint(line)
            datapoint_array.append(dp)

for item in datapoint_array:
    print(item.hz125)
