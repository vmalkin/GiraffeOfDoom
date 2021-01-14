"""
To create simple scatterplot of S4 data
"""
import datetime

timeformat = '%Y-%m-%d %H:%M'

def posix2utc(posixtime):
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime

# query format:
# ('8', posixtime, 21.0, 238.84615384615384, 11.68933, 18.5)
def wrapper(queryresults):
    print(queryresults)