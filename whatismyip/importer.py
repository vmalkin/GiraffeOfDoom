import urllib.request as webreader

# this bit gets the info from remote source. This fucntion will probably have to be customised to deal with
# any data format, but must return an array with each element of the format: ("UTC datetime", datareading)

def importdata():
    url = "https://api.ipify.org/"
    response = webreader.urlopen(url)
    ipaddress = response.read().decode("utf-8")

    return ipaddress



# END of preparser