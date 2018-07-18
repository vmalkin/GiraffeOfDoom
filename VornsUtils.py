import time
import datetime
# #################################################################################
# save an array to file
# #################################################################################
def csv_save(filename, array_name):
    # export array to array-save file
    try:
        with open(filename, 'w') as w:
            for item in array_name:
                w.write(item + '\n')
    except IOError:
        print("WARNING: There was a problem accessing " + filename)
        logging.warning("WARNING: File IO Exception raised whilst accessing file: " + filename)

# Function to load CSV. Returns a list    
def csv_load(csvfilename):
    """
    Load a CSV file.
    """
    returnlist = []
    with open(csvfilename, "r") as f:
        for line in f:
            line = line.strip()
            returnlist.append(line)
    return returnlist

# convert the internal posx_date to UTC format
def posix2utc(posix_string):
    utctime = time.gmtime(int(float(posix_string)))
    utctime = time.strftime('%Y-%m-%d %H:%M', utctime)
    return utctime

def utc2posix(utcstring):
    pass