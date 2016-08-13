import constants as k
import ArrayManager as am
from decimal import Decimal, getcontext
import os
import time

# append output to a file.
def createoutputfile(texttowrite, filename):
    try:
        with open(filename, 'a') as f:
            f.write(texttowrite + "\n")
    except IOError:
        print("WARNING: There was a problem accessing " + k.OUTPUT_FILE)

# def minstohours(minutevalue):
#     if minutevalue <= 60:
#         returnvalue = str(minutevalue) + " minutes"
#     else:
#         returnvalue = str(round((minutevalue/60),1)) + " hours"
#     return returnvalue

# ###############################################
# Main Parts STarts Here
# purge old file for writing...
# ###############################################

while True:
    try:
        importarray = []
        # Load up file into array
        # print(k.FILE_BINNED_MINS)
        importarray = am.CreateRawArray(k.FILE_BINNED_MINS)

        # remove the first line which may contain text header
        importarray.pop(0)

        # what is the size of the sliding window we want to use to show that a blip happened in a certain interval?
        windowsizeminutes = 60
        windowinterval = k.MAG_READ_FREQ * windowsizeminutes

        try:
            os.remove(k.OUTPUT_FILE)
        except OSError:
            print("WARNING: could not delete " + k.OUTPUT_FILE)

        # Possible create a sub-list to only get values for the lasty 2 hours??

        # Reverse array, make the most recent time index[0]
        importarray.reverse()

        hr = 0
        outputlist = []
        datestring = importarray[0].dateTime

        for i in range(0, len(importarray), windowinterval):
            maxv = Decimal(0)
            minv = Decimal(0)

            if i + windowinterval < len(importarray):
                for j in range(i, i + windowinterval):
                    # determin max and min values for this window interval
                    if Decimal(importarray[j].raw_x) >= maxv:
                        maxv = Decimal(importarray[j].raw_x)
                    elif Decimal(importarray[j].raw_x) <= minv:
                        minv = Decimal(importarray[j].raw_x)

                    # calculate the variation
                hr = hr + 1
                fieldstrength = Decimal(0)
                fieldstrength = maxv - minv

                if fieldstrength <= Decimal(k.MAG_THRESHOLD_NORMAL):
                    spancolour = k.COLOUR_N
                elif fieldstrength > Decimal(k.MAG_THRESHOLD_NORMAL) and fieldstrength <= Decimal(k.MAG_THRESHOLD_MEDIUM):
                    spancolour = k.COLOUR_N_M
                elif fieldstrength > Decimal(k.MAG_THRESHOLD_NORMAL) and fieldstrength <= Decimal(k.MAG_THRESHOLD_HIGH):
                    spancolour = k.COLOUR_M_H
                    # this is an alert condition
                elif fieldstrength > Decimal(k.MAG_THRESHOLD_HIGH):
                    spancolour = k.COLOUR_H
                    # this is an alert condition

                spantag = "<td style=\"border-radius: 3px; text-align: center; padding: 2px; background-color: " + spancolour + "\">"
                outputtext = spantag + str(hr) + " hr<br>ago" + "</td>"
                print(outputtext)
                outputlist.append(outputtext)


        outputlist.reverse()
        createoutputfile("<table style=\" width: 95%; font-size: 0.7em;\"><tr>",k.OUTPUT_FILE)
        for item in outputlist:
            createoutputfile(item, k.OUTPUT_FILE)
        createoutputfile("</tr></table>",k.OUTPUT_FILE)

        createoutputfile("<div style=\"font-size: 0.7em;\">",k.OUTPUT_FILE)
        createoutputfile("<br><span style=\"background-color: " + k.COLOUR_N + "\">Normal</span> and ", k.OUTPUT_FILE)
        createoutputfile("<span style=\"background-color: " + k.COLOUR_N_M + "\">Minor</span> activity are typical.<br>", k.OUTPUT_FILE)
        createoutputfile("Continuous intervals of <span style=\"background-color: " + k.COLOUR_M_H + "\">Moderate</span>", k.OUTPUT_FILE)
        createoutputfile("and <span style=\"background-color: " + k.COLOUR_H + "\">HIGH</span> activity may mean active aurora. Updates every 10 minutes.<br><br>", k.OUTPUT_FILE)
        createoutputfile("<i>Last updated at " + datestring + "</i>", k.OUTPUT_FILE)
        createoutputfile("</div>",k.OUTPUT_FILE)

    except:
        print("dreadfully lazy try/except here!")

    time.sleep(600)