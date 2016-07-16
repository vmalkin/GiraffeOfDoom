from decimal import Decimal, getcontext
import DataPoint


# #################################################################################
# Median filter based on 3 values
#
# #################################################################################
def median_filter_3values(arraydata):
    outputarray = []

    for i in range(1,len(arraydata)-1):
        xlist = []
        ylist = []
        zlist = []

        for j in range(-1,2):    # -1, 0, 1
            k = i + j
            xlist.append(arraydata[k].raw_x)
            ylist.append(arraydata[k].raw_y)
            zlist.append(arraydata[k].raw_z)

        xlist.sort()
        ylist.sort()
        zlist.sort()

        dp = DataPoint.DataPoint(arraydata[i].dateTime, xlist[1],ylist[1], zlist[1])

        outputarray.append(dp)

    return outputarray

# #################################################################################
# Create the smoothed data array and write out the files for plotting.
# We will do a running average based on the running average time in minutes and the number
# readings per minute
#
# we will divide this number evenly so our average represents the midpoint of these
# readings.
# #################################################################################
def running_average(input_array, AVERAGING_TIME):
    getcontext().prec = 5
    displayarray = []

    # This figure MUST be an even number. Check your constants.
    AVERAGING_TIME = 9
    AVERAGING_TIME_HALF = int((AVERAGING_TIME - 1) / 2)
    data_temp = []
    # NOW average the cumulative array, smooth out the blips
    if len(input_array) > AVERAGING_TIME:
        for i in range(AVERAGING_TIME_HALF + 1, len(input_array) - AVERAGING_TIME_HALF - 1):
            dataa = 0
            datab = 0
            for j in range(1 - AVERAGING_TIME_HALF, 1 + AVERAGING_TIME_HALF):
                datasplit = input_array[i+j].split(",")
                datetime = datasplit[0]
                dataa = dataa + Decimal(datasplit[1])
                datab = datab + Decimal(datasplit[2])
            dataa = Decimal(dataa / AVERAGING_TIME)
            datab = Decimal(datab / AVERAGING_TIME)
            datastring = datetime +","+ str(dataa) +","+ str(datab)
            data_temp.append(datastring)
        displayarray = data_temp

    else:
        displayarray = input_array

    return displayarray
