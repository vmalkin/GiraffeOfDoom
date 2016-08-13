import constants as k
import ArrayManager as am
from decimal import Decimal, getcontext
import mysql.connector as mariadb
import os
import time
import re
import DataPoint


#########################################################################################################
# Alert/Blip Detection
# This routine takes in an array of magnetometer readings binned in minute intervals for the last 24 hours
# It parses this array, determins the strength of the field for hourly intervals and generates an
# HTML chunk for simple, colour-coded display of the field strength for the past 12 hours
#########################################################################################################


# append output to a file.
def createoutputfile(texttowrite, filename):
    try:
        with open(filename, 'a') as f:
            f.write(texttowrite + "\n")
    except IOError:
        print("WARNING: There was a problem accessing " + k.OUTPUT_FILE)

# Function to get last hours of data from Database
def getdata():
    temparray = []
    try:
        dbConnection = mariadb.connect(host='127.0.0.1', port=3307,user='TestUser', password='TestPassword', database='helios_DB_005')
        print("INFO: Connect to remote DB ok.")

        # Instantiate the cursor object to interact with the database
        cursor = dbConnection.cursor()

        # send query
        # The result of the query is stored in a list called "cursor." To test the result you can print
        # it with a simple for loop, but for better formatting use Python's string formatting method:
        try:
            # http://stackoverflow.com/questions/7929364/python-best-practice-and-securest-to-connect-to-mysql-and-execute-queries
            cursor.execute("SELECT * FROM DataF WHERE DataF.timestamp > DATE_SUB(NOW(), INTERVAL 60 MINUTE)")
            # grab the result of the query
            data = cursor.fetchall()

            # Parse out each row, and append to our temp array
            for row in data:
                # print(row)
                temparray.append(row)

        except mariadb.Error as error:
            errorMsg = "SQL Select Error: {}".format(error)
            print(errorMsg) # SQL errors will be displayed on console. Probably need to log this.
            dbConnection.rollback() # rollback the query
            dbConnection.close()

        except:
            errorMsg = "ERROR: Unhandled MySQL exception error!"
            print(errorMsg)
            dbConnection.close()

        # CLOSE the connection to the DB. We don't want open connections dangling everywhere now, do we?
        dbConnection.close()

    except mariadb.Error as error:
        errorMsg = "ERROR: MySQL connection error " + str(error.errno)
        print(errorMsg)
        dbConnection.close()

    rawdata = []
    for item in temparray:
        dp = DataPoint.DataPoint(str(item[1]),str(item[2]),0,0)
        rawdata.append(dp)

    return rawdata

# #################################################################################
# Create binned minutely averages
# to be used for experimental data/sensor merge project
# #################################################################################
def binnedaverages(readings):
    # Get each datapoint to print out it's values. Use re to split this on spaces, commas, and semi colons.
    # ['2016-05-08', '03', '34', '37.61', '58835.20']
    hAvg = Decimal(0)

    counter = 0
    binnedvalues = []

    # Open the readings array
    for j in range(0, len(readings)-1):
        # Get the first datapoint from the array, so we get the current minute...
        dpvalues = re.split(r'[\s,:]', readings[j].print_values())
        nowminute = dpvalues[2]
        datetime = dpvalues[0] + " " + dpvalues[1] + ":" + nowminute

        # get the value for the next minute
        dpvalues1 = re.split(r'[\s,:]', readings[j + 1].print_values())
        nextminute = dpvalues1[2]

        # We are still summing values...
        if nowminute == nextminute and counter < k.MAG_READ_FREQ - 1:
            hAvg = hAvg + Decimal(dpvalues[4])
            counter = counter + 1

        # we have added up all the values for the minute and done the correct num of iterations
        # based on the frequency of the magnetometers output
        elif nowminute != nextminute and counter == k.MAG_READ_FREQ - 1:
            hAvg = hAvg + Decimal(dpvalues[4])

            # print(nowminute + " " + str(xAvg))
            hAvg = hAvg / Decimal(k.MAG_READ_FREQ)

            dp = DataPoint.DataPoint(datetime, xAvg, 0, 0,)
            binnedvalues.append(dp)

            xAvg = 0
            counter = 0

        # Otherwise we do not have the correct number of iterations for the minute, ignore this.
        else:
            xAvg = 0
            counter = 0

    return binnedvalues


# ###############################################
# Main Parts STarts Here
# purge old file for writing...
# ###############################################
while True:
    try:
        # Run the DB query
        sqldata = getdata()

        importarray = binnedaverages(sqldata)

        print(importarray)

        # importarray = binnedaverages(sqldata)
        # print("Import array is " + len(importarray))

        # remove the first line which may contain text header
        importarray.pop(0)

        # what is the size of the sliding window we want to use to show that a blip happened in a certain interval?
        windowsizeminutes = 60
        windowinterval = k.MAG_READ_FREQ * windowsizeminutes

        try:
            os.remove(k.OUTPUT_FILE)
        except OSError:
            print("WARNING: could not delete " + k.OUTPUT_FILE)

        # Reverse array, make the most recent time index[0]
        importarray.reverse()

        hr = 0
        outputlist = []
        datestring = importarray[0].dateTime

        # Stepping thru the array, in chunks of an hour at a time (Windowinterval)...
        for i in range(0, len(importarray), windowinterval):
            maxv = Decimal(0)
            minv = Decimal(0)

            # for each hour, calculate the max and min values for the magnetometer readings.
            if i + windowinterval < len(importarray):
                for j in range(i, i + windowinterval):
                    # determin max and min values for this window interval
                    if Decimal(importarray[j].raw_x) >= maxv:
                        maxv = Decimal(importarray[j].raw_x)
                    elif Decimal(importarray[j].raw_x) <= minv:
                        minv = Decimal(importarray[j].raw_x)

                # From the max and min magnetometer values, calculate the field strength for the hour
                hr = hr + 1
                fieldstrength = Decimal(0)
                fieldstrength = maxv - minv

                # Codeblock to catagorise the fieldstrength readings as normal, minor activity, High activity, etc...
                # It is in here that we could have some kind of automatic alert be generated if the threshold is reached
                # in the current hour.
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

        # This codeblock just generates the HTML for the display on the webpage.
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

    # Pause the execution of this routine for 10 minutes...
    time.sleep(600)