#!usr/bin/python
import os
import logging
import constants as k
import time
from random import randint
import shutil as s

RANDOM_SECS = 10                # To randomise the minutes delay
DELAY_SHORT_INTERVAL = 30       # THE DELAY INTERVAL FOR FILE COPYING
delay_interval = 0              # used to trigger the copy of larger files less frequently


# Setup error/bug logging
logging.basicConfig(filename="pubError.log", format='%(asctime)s %(message)s')

# setup file paths
# Set up file structure for Data logs. Linux systems might need use of the mode arg to set correct permissions.
try:
    os.makedirs("publish")
    print("Created publishing directory")
except:
    if not os.path.isdir("publish"):
        print("Unable to create publisher directory")
        logging.critical("CRITICAL ERROR: Unable to create publisher directory")

def try_publish(filename):
    try:
        s.copy("graphing/" + filename, "publish")
        print("Published " + filename)
    except s.Error as e:
        print('Error: %s' % e)
        logging.critical('Error: %s' % e)

while True:
    timedelay = DELAY_SHORT_INTERVAL + randint(0,RANDOM_SECS)
    time.sleep(timedelay)
    try_publish("04hr.csv")

    delay_interval = delay_interval + 1
    if delay_interval >= 5:
        try_publish("24hr.csv")
        try_publish("diffs.csv")
        delay_interval = 0
	
    print("Interval: " + str(timedelay) + " seconds")
    print(" ")



