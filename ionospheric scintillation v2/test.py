import re
import constants as k
import mgr_comport
import time
import os
import sqlite3
import datetime
import logging
from statistics import mean, stdev
from threading import Thread
import mgr_database
import mgr_plot
import numpy as np
from calendar import timegm

def utc2posix(utcstring, timeformat):
    utc_time = time.strptime(utcstring, timeformat)
    epoch_time = timegm(utc_time)
    return epoch_time

utctime = "2023-02-20 00:00"
starttime = utc2posix(utctime, '%Y-%m-%d %H:%M')
day = 60 * 60 * 24 * 14
actualstart = starttime - day

alt = 40
# The result of the query gets passed into all plotting functions
result = mgr_database.qry_get_last_24hrs(actualstart, alt)
result = np.array(result)

mgr_plot.wrapper(result, k.comport)




