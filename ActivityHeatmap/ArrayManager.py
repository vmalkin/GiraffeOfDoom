import DataPoint
import os.path


__author__ = 'vaughn'

# #################################################################################
# Create the raw datapoint array from the save file
# #################################################################################
def CreateRawArray(sourcefile):
    print("Loading " + sourcefile)
    readings = []
    # Check if exists CurrentUTC file. If exists, load up Datapoint Array.
    if os.path.isfile(sourcefile):
        with open(sourcefile) as e:
            for line in e:
                line = line.strip() # remove any trailing whitespace chars like CR and NL
                values = line.split(",")
                dp = DataPoint.DataPoint(values[0], values[1],0,0)
                readings.append(dp)
        print("Array loaded from file. Size: " + str(len(readings)) + " records")
    else:
        print("No save file loaded.")

    return  readings



