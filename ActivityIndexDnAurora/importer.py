import urllib.request as webreader

# this bit gets the info from remote source. This fucntion will probably have to be customised to deal with
# any data format, but must return an array with each element of the format: ("UTC datetime", datareading)

def importdata():
    url = "http://Dunedinaurora.nz/Service24CSV.php"
    importarray = []

    response = webreader.urlopen(url)
    for item in response:
        logData = str(item, 'ascii').strip()
        logData = logData.split(",")
        dp = logData[0] + "," + logData[1]
        importarray.append(dp)

    return importarray

# END of preparser