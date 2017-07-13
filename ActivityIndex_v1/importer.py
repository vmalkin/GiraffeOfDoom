import urllib.request as webreader
import os
# this bit gets the info from remote source. This fucntion will probably have to be customised to deal with
# any data format, but must return an array with each element of the format: ("UTC datetime", datareading)

# # #################################################################################
# # Create the raw datapoint array from the save file
# # #################################################################################
def importdata(sourcefile):
    print("Loading " + sourcefile)
    readings = []
    # Check if exists CurrentUTC file. If exists, load up Datapoint Array.
    if os.path.isfile(sourcefile):
        with open(sourcefile) as e:
            for line in e:
                line = line.strip() # remove any trailing whitespace chars like CR and NL
                values = line.split(",")
                dp = values[0] + "," + values[1]
                readings.append(dp)
        print("Array loaded from file. Size: " + str(len(readings)) + " records")
    else:
        print("No save file loaded.")

    return  readings

# def importdata():
#     url = "http://Dunedinaurora.nz/Service24CSV.php"
#     importarray = []
#
#     response = webreader.urlopen(url)
#     for item in response:
#         logData = str(item, 'ascii').strip()
#         logData = logData.split(",")
#         dp = logData[0] + "," + logData[1]
#         importarray.append(dp)
#
#     return importarray

# END of preparser