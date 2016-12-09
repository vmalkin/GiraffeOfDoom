import constants as k
import ArrayManager as am
from decimal import Decimal, getcontext
import mysql.connector as mariadb
import os
import time
import re



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
    interval = str(60)
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
            cursor.execute("SELECT * FROM DataF WHERE DataF.timestamp > DATE_SUB(NOW(), INTERVAL " + interval + " MINUTE)")
            # cursor.execute("SELECT * FROM DataF WHERE DataF.timestamp > DATE_SUB(NOW(), INTERVAL 60 MINUTE)")
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

    # MAssage the temp array into something more sensible
    outputlist = []
    for item in temparray:
        # Convert the datetime and mag readings.
        appendstring = str(item[1]) + "," + str(item[2])
        outputlist.append(appendstring)

    return outputlist

# #################################################################################
# Create binned minutely averages
# to be used for experimental data/sensor merge project
# #################################################################################
def splitarray(readings):
    # Get each datapoint to print out it's values. Use re to split this on spaces, commas, and semi colons.
    # ['2016-05-08', '03', '34', '37.61', '58835.20']
    binnedvalues = []

    # Open the readings array
    for i in range(1, len(readings)-1):
        # Get the first datapoint from the array, so we get the current minute...
        dpvalues = re.split(r'[\s,:]', readings[i])

        appendstring = ""
        for item in dpvalues:
            appendstring = appendstring + item + ","

        # get rid of the trailing comma
        appendstring = appendstring[:len(appendstring) - 1]
        binnedvalues.append(appendstring)

    # we now have an array where the datetime values are comma separated. Return this
    return binnedvalues


# ###############################################
# Main Parts STarts Here
# purge old file for writing...
# ###############################################

KIndex = []
while True:
    # Run the DB query
    sqldata = getdata()
    splitdata = splitarray(sqldata)

    for item in splitdata:
        print(item)

    print("Waiting for next run")
    time.sleep(600)