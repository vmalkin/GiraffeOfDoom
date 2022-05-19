# YYYY-MM-DD hh:mm:ss,125hz,240hz,410hz,760hz,1800hz,4300hz,9000hz
# 2022-01-15 04:13:34,36.243,33.482,23.342,21.961,17.429,3.902,-3.328
hissfile = "hiss.csv"

class DataPoint:
    def __init__(self, data_csv):
        self.utc = data_csv[0]
        self.hz125 = data_csv[2]
        self.hz240 = data_csv[3]
        self.hz410 = data_csv[4]
        self.hz760 = data_csv[5]
        self.hz1800 = data_csv[6]
        self.hz4300 = data_csv[7]
        self.hz9000 = data_csv[8]

        self.diff125 = 0
        self.diff240 = 0
        self.diff410 = 0
        self.diff760 = 0
        self.diff1800 = 0
        self.diff4300 = 0
        self.diff9000 = 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with open(hissfile, "r") as h:
        for line in h:
            pass
