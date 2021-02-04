import time
import importer
import os
import urllib.request as webreader

# this bit gets the info from remote source. This fucntion will probably have to be customised to deal with
# any data format, but must return an array with each element of the format: ("UTC datetime", datareading)

def importdata():
    url = "https://api.ipify.org/"
    response = webreader.urlopen(url)
    ipaddress = response.read().decode("utf-8")

    return ipaddress

def savetofile(datastring):
    savefile = "/home/vmalkin/Magnetometer/publish/ip.txt"
    # savefile = "ip.txt"

    try:
        with open (savefile,'w') as f:
            f.write(datastring)
    except IOError:
        print("WARNING: There was a problem accessing " + savefile)

# ###############################################
# Main Parts STarts Here
# ###############################################
if __name__ == "__main__":
    ipaddress = importer.importdata()
    print(ipaddress)
    savetofile(ipaddress)
