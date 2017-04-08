import time
import importer
import os

def savetofile(datastring):
    savefile = "ip.txt"
    try:
        os.remove(savefile)
    except OSError:
        print("WARNING: could not delete " + savefile)
    try:
        with open (savefile,'w') as f:
            f.write(datastring)
    except IOError:
        print("WARNING: There was a problem accessing " + savefile)

# ###############################################
# Main Parts STarts Here
# ###############################################

while True:
    ipaddress = importer.importdata()
    print(ipaddress)
    savetofile(ipaddress)

    time.sleep(10800)