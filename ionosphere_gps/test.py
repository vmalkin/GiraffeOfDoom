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
import mgr_heatmaps
import numpy as np
from calendar import timegm

starttime = time.time() - (60 * 60 * 24 * 100)
alt = 40
# The result of the query gets passed into all plotting functions
result2 = mgr_database.qry_get_last_24hrs(starttime, alt)
result2 = np.array(result2)
mgr_heatmaps.wrapper(result2, k.comport)



