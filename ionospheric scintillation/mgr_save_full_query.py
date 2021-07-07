#  The raw query output is saved as an CSV file
import datetime

timeformat = '%Y-%m-%d %H:%M'

def posix2utc(posixtime):
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime

# query format:
# ('satID', posixtime, alt, az, s4, snr)
def wrapper(queryresults):
    with open("full_query.csv", 'w') as f:
        for item in queryresults:
            d = str(item[0]) + "," +str(posix2utc(item[1])) + "," +str(item[2]) + "," +str(item[3]) + "," +str(item[4]) + "," +str(item[5])
            f.write(d + '\n')
        f.close()