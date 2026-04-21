import constants as k
import standard_stuff
import gzip

def csv_save(parseddata):
    for item in parseddata:
        print(f"{standard_stuff.posix2utc(item[0], '%Y-%m-%d')}.csv")