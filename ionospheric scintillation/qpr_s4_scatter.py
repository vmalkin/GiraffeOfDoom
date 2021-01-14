"""
To create simple scatterplot of S4 data
"""
import datetime

timeformat = '%Y-%m-%d %H:%M'

def posix2utc(posixtime):
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime

def save_s4(filename, data):
    try:
        with open(filename, 'w') as f:
            f.write("Datetime UTC, S4 Scintillation Index" + '\n')
            for result in data:
                f.write(result + '\n')
        f.close()
        print("S4 csv"
              " file written")
    except PermissionError:
        print("CSV file being used by another app. Update next time")

# query format:
# ('satID', posixtime, alt, az, s4, snr)
def wrapper(queryresults):
    datalist = []
    for item in queryresults:
        dt = item[1]
        dt = posix2utc(dt)
        da = str(item[4])

        dp = dt + "," + da
        datalist.append(dp)
    save_s4("s4.csv", datalist)