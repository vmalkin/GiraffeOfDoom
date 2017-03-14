import pickle
import constants as k
from datetime import datetime
import os


# load pickle file and return the min-max array
def loadpickle(file):
    try:
        dataarray = pickle.load(open(file, "rb"))
        # print("Loaded values from file")
    except:
        dataarray = []
        print("No file to load. Creating values of zero")

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

# append output to a file.
def fileoutput(texttowrite, filename):
    try:
        with open(filename, 'a') as f:
            f.write(texttowrite + "\n")
    except IOError:
        print("WARNING: There was a problem")

def createcolour(value):
    if value == k.NULLBIN:
        value = 0

    if value < 0.65:
        red = 24
        green = 171
        blue = 28

    if value >= 0.65 and value < 0.9:
        red = 255
        green = 118
        blue = 17

    if value >= 0.9:
        red = 255
        green = 0
        blue = 0

    rd = 255 - ((value) * (255 - red))
    gr = 255 - ((value) * (255 - green))
    bl = 255 - ((value) * (255 - blue))

    # Based on the value (0, quiet; 1 active) adjust the colours so that least activity will be ffffff
    # and most activity will be the supplied colour.
    # Convert decimal values to hex
    rd = str(hex(int(rd)))
    rd = rd.split("x")
    if len(rd[1]) == 1:
        rd = "0" + str(rd[1])
    else:
        rd = str(rd[1])

    gr = str(hex(int(gr)))
    gr = gr.split("x")
    if len(gr[1]) == 1:
        gr = "0" + str(gr[1])
    else:
        gr = str(gr[1])

    bl = str(hex(int(bl)))
    bl = bl.split("x")
    if len(bl[1]) == 1:
        bl = "0" + str(bl[1])
    else:
        bl = str(bl[1])

    # create hex colour string
    finalhex = str(rd) + str(gr) + str(bl)
    # print(finalhex)
    return finalhex


def htmlcreate(array):
    htmlfile = k.OUTPUTFILE
    try:
        os.remove(htmlfile)
    except OSError:
        print("WARNING: could not delete " + htmlfile)

    fileoutput('<table style=" width: 95%; font-size: 0.5em;">', htmlfile)

    fileoutput("<tr>", htmlfile)


    for i in range(0, len(array)):
        c1 = '<td style="border-radius: 3px; text-align: center; padding: 2px; background-color: #'
        c2 = '">'
        hexcode = createcolour(array[i])
        c3 = c1 + hexcode + c2
        fileoutput(c3, htmlfile)

        # cell content
        dp = str(array[i])
        dp = dp[:4]
        hr = 23 - i
        cellstring = str(hr) + " hrs ago<br><b>" + str(dp) + "</b>"
        fileoutput(str(cellstring), htmlfile)

        fileoutput("</td>", htmlfile)

    c1 = '<td style="border-radius: 3px; text-align: center; padding: 2px;">'
    c2 = '</td>'
    c3 = c1 + k.STATION_NAME + c2
    fileoutput(c3, htmlfile)

    fileoutput("</tr>", htmlfile)

    fileoutput("</table>", htmlfile)
    currentdt = datetime.utcnow()
    # stringtxt = '<p style="font-size: 0.7em;">Last updated at ' + str(currentdt) + " UTC.</p>"
    # fileoutput(stringtxt, htmlfile)

# wrapper function to run this library. Called from the main script
def main(livedata):
    # minmax only contains 2 values: [minv, maxv]. These are the highest and lowest recorded results to date. These
    # are appended to the max and min arrays and form the long-term "memory" of highest and lowest values for the
    # device. Outlier data will be appended the should be missed when grabbing the median value
    minmax = loadpickle("minmax.pkl")
    dateminmax = loadpickle("dateminmax.pkl")

    if len(dateminmax) == 0:
        currentdt = datetime.utcnow()
        dateminmax.append(currentdt)
        dateminmax.append(currentdt)

    # get the current max and min values from the live data. if the minmax array is empty, then start with
    # whatever minmax values we can find
    if len(minmax) == 0:
        d = findarraymin(livedata)
        minmax.append(d)
        d = findarraymax(livedata)
        minmax.append(d)
    # Otherwise compare current stored values with live. The assumption is larger values than stored are valid...
    else:
        dtm = datetime.utcnow()
        livemin = findarraymin(livedata)
        if livemin <= minmax[0]:
            minmax[0] = livemin
            dateminmax[0] = dtm

        livemax = findarraymax(livedata)
        if livemax >= minmax[1]:
            minmax[1] = livemax
            dateminmax[1] = dtm

    maxvalue = minmax[1]
    minvalue = minmax[0]
    heatmaparray = heatmapprocess(maxvalue, minvalue, livedata)
    htmlcreate(heatmaparray)

    print("Low value of " + str(minmax[0]) + " recorded at " + str(dateminmax[0]))
    print("High value of " + str(minmax[1]) + " recorded at " + str(dateminmax[1]))

    savepickle(minmax, "minmax.pkl")
    savepickle(dateminmax, "dateminmax.pkl")

    return heatmaparray