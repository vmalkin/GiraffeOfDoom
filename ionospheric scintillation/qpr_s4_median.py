"""
create a graph of the median S4 values for each time bin
Typically I would create preset bin objects for a time interval and populate an array in each
object and use the median value of that array
"""
from statistics import median

def save_s4(filename, data):
    try:
        with open(filename, 'w') as f:
            f.write("Datetime UTC, Median S4 Index" + '\n')
            for result in data:
                f.write(result + '\n')
        f.close()
        print("Median S4 csv file written")
    except PermissionError:
        print("CSV file being used by another app. Update next time")

# query format:
# ('satID', posixtime, alt, az, s4, snr)
def wrapper(queryresults):
    pass