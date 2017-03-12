import pickle
import constants as k

# load pickle file and return the min-max array
def loadpickle(file):
    try:
        dataarray = pickle.load(open(file, "rb"))
        # print("Loaded values from file")
    except:
        dataarray = [0,0]
        print("No minmax file to load. Creating values of zero")

    return dataarray


# save array to pickle file. Prints a result
def savepickle(array, file):
    try:
        pickle.dump(array, open(file, "wb"))
        print("Save ok")
    except:
        print("ERROR saving array")


# return the median value of an list
# the array is a list of single values
# this function could also be used to reset a large array to a seed value as part of a periodic
# pruning process to manage the size of the arrays.
def findarraymedian(array):
    if len(array) > 2:
        medpoint = int(len(array) / 2)
    else:
        medpoint = 0

    if medpoint == k.NULLBIN:
        medianvalue = 0
    else:
        medianvalue = array[medpoint]

    return medianvalue


# find min and max values in a list
def findarraymin(array):
    values = []
    for item in array:
        if item == k.NULLBIN:
            item = 0
        dp = float(item)
        values.append(dp)

    values.sort()
    minvalue = values[0]

    if minvalue == k.NULLBIN:
        minvalue = 0

    return minvalue


def findarraymax(array):
    values = []
    for item in array:
        if item == k.NULLBIN:
            item = 0

        dp = float(item)
        values.append(dp)

    values.sort()
    values.reverse()
    maxvalue = values[0]

    if maxvalue == k.NULLBIN:
        maxvalue = 0

    return maxvalue

# this is the functon that will scale the data according to the _median_ max and min values. It will return
# a list
def heatmapprocess(maxv, minv, array):
    returnarray = []

    window = maxv - minv

    # If we have sufficient max and min values to calculate a meaningful result
    if window != 0:
        # then calculate values....
        for item in array:
            if item != k.NULLBIN:
                dp = float(item) - minv
                dp = dp / window
                returnarray.append(dp)
            else:
                returnarray.append(k.NULLBIN)
    else:
        print("ERROR: window value is too small: " + str(window))

    # for item in array:
    #     dp = str(item) + "," + str(minv) + "," + str(maxv)
    #     returnarray.append(dp)

    return returnarray


# wrapper function to run this library. Called from the main script
def main(livedata):
    # load the max and min arrays from file
    maxarray = loadpickle("max.p")
    print("MAX: " + str(maxarray))

    minarray = loadpickle("min.p")
    print("MIN: " + str(minarray))

    # minmax only contains 2 values: [minv, maxv]. These are the highest and lowest recorded results to date. These
    # are appended to the max and min arrays and form the long-term "memory" of highest and lowest values for the
    # device. Outlier data will be appended the should be missed when grabbing the median value
    minmax = loadpickle("minmax.p")
    print("LIVE LOW & HIGH: " + str(minmax))

    # get the current max and min values from the live data
    livemin = findarraymin(livedata)
    if livemin <= minmax[0]:
        minmax[0] = livemin

    livemax = findarraymax(livedata)
    if livemax >= minmax[1]:
        minmax[1] = livemax

    # append these values to the max and min arrays
    maxarray.append(minmax[1])
    minarray.append(minmax[0])

    # get the current median max and min values from the saved data
    maxvalue = findarraymedian(maxarray)
    minvalue = findarraymedian(minarray)

    # create the processed data for display as a heatmap
    # print("High and low values are " + str(maxvalue) + " " + str(minvalue))
    heatmaparray = heatmapprocess(maxvalue, minvalue, livedata)

    # Prune the max/min arrays if too large. Seed new array with the current median values
    prunesize = 20
    if len(maxarray) > prunesize:
        maxarray = []
        maxarray.append(maxvalue)
    if len(minarray) > prunesize:
        minarray = []
        minarray.append(minvalue)

    # Save the max and min arrays
    savepickle(maxarray, "max.p")
    savepickle(minarray, "min.p")
    savepickle(minmax, "minmax.p")

    return heatmaparray