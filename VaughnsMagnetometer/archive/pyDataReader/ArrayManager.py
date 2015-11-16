import DataPoint
import constants as k
import os.path
import logging
import OutputFileManager as ofm
import math

__author__ = 'vaughn'

# #################################################################################
# Create the raw datapoint array from the save file
# #################################################################################
def CreateOutputFileArray(RawArray):
    # first setup an array to store differences
    diffsArray = []

    # Calculate the differences between readings
    for i in range(1,len(RawArray)):
        datetime = RawArray[i].dateTime

        # here we deal with flipping. differences should be in the order of 10s. It we're seeing 100s, there's an issue.
        diffX = float(RawArray[i].rawMagX) - float(RawArray[i-1].rawMagX)
        if math.sqrt(math.pow(diffX,2)) > k.MAG3110_FLIP:
            diffX = 0

        diffY = float(RawArray[i].rawMagY) - float(RawArray[i-1].rawMagY)
        if math.sqrt(math.pow(diffY,2)) > k.MAG3110_FLIP:
            diffY = 0

        diffZ = float(RawArray[i].rawMagZ) - float(RawArray[i-1].rawMagZ)
        if math.sqrt(math.pow(diffZ,2)) > k.MAG3110_FLIP:
            diffZ = 0

        diffpoint = DataPoint.DataPoint(datetime, diffX, diffY, diffZ)

        diffsArray.append(diffpoint)

    # Now convert the array from difference to a cumulative sum. This is what will be plotted.
    cumulativeArray = []
    plotX = 0
    plotY = 0
    plotZ = 0

    for i in range(0,len(diffsArray)):
        datetime = diffsArray[i].dateTime
        plotX = plotX + diffsArray[i].rawMagX
        plotY = plotY + diffsArray[i].rawMagY
        plotZ = plotZ + diffsArray[i].rawMagZ
        plotpoint = DataPoint.DataPoint(datetime, plotX, plotY, plotZ)
        cumulativeArray.append(plotpoint)

    # NOW average the cumulative array, smooth out the blips
    displayarray = []
    
    for i in range( len(cumulativeArray)-1, k.MAG_RUNNINGAVG_COUNT, -1):
        xvalue = 0
        yvalue = 0
        zvalue = 0
    
        for j in range(0, k.MAG_RUNNINGAVG_COUNT - 1):
            xvalue = xvalue + cumulativeArray[i-j].rawMagX
            yvalue = yvalue + cumulativeArray[i-j].rawMagY
            zvalue = zvalue + cumulativeArray[i-j].rawMagZ
    
        xvalue = xvalue / k.MAG_RUNNINGAVG_COUNT
        yvalue = yvalue / k.MAG_RUNNINGAVG_COUNT
        zvalue = zvalue / k.MAG_RUNNINGAVG_COUNT
    
        displaypoint = DataPoint.DataPoint(cumulativeArray[i].dateTime, xvalue, yvalue, zvalue)
        displayarray.append(displaypoint)
    
    # The display array is back to front, so reverse.
    displayarray.reverse()
    
    print("Datapoint Values: " + str(displayarray[len(displayarray)-1].rawMagX))
    # create the graphing files
    ofm.Create24(displayarray)
    ofm.Create4(displayarray)


# #################################################################################
# Create the raw datapoint array from the save file
# #################################################################################
def CreateRawArray(readings):
    # Check if exists CurrentUTC file. If exists, load up Datapoint Array.
    if os.path.isfile(k.FILE_ROLLING):
        with open(k.FILE_ROLLING) as e:
            for line in e:
                line = line.strip() # remove any trailing whitespace chars like CR and NL
                values = line.split(",")
                # Data point takes: dateTime, rawMagX, rawMagY, rawMagZ
                dp = DataPoint.DataPoint(values[0], values[1], values[2], values[3])
                readings.append(dp)
        print("Array loaded from file. Size: " + str(len(readings)) + " records")
    else:
        print("No save file loaded. Using new array.")

# #################################################################################
# Save the raw datapoint array to the save file
# #################################################################################
def SaveRawArray(readings):
    # export array to array-save file
        try:
            with open (k.FILE_ROLLING, 'w') as w:
                for dataObjects in readings:
                    w.write(dataObjects.dateTime + "," + dataObjects.rawMagX + "," + dataObjects.rawMagY + "," + dataObjects.rawMagZ + '\n')
        except IOError:
            print("WARNING: There was a problem accessing " + k.FILE_ROLLING)
            logging.warning("WARNING: File IO Exception raised whilst accessing file: " + k.FILE_ROLLING)

# #################################################################################
#  Create a datapoint, run analysis,
# #################################################################################
def AppendDataPoint(datapoint, readingsArray):
    # create a datapoint object

    # perform the Analysis on the datapoint if the array is big enough
    if (len(readingsArray) > k.MAG_RUNNINGAVG_COUNT - 1):
        # datapoint.CalcDifference(readingsArray[len(readingsArray) - 1])
        pass

    # Append the datapoint to the array. Prune off the old datapoint if the array is 24hr long
    if(len(readingsArray) < k.MAG_READ_FREQ * 60 * 24):
        readingsArray.append(datapoint)
    else:
        readingsArray.pop(0)
        readingsArray.append(datapoint)

    # we want to return the datapoint back to the calling method


