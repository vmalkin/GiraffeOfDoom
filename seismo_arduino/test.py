import mgr_database
import time
import constants as k
import plotter_helicorder
import csv

from plot_master import result_1d

with open('datagenerator.csv', 'r') as d:
    result_1d = csv.reader(d)


print(len(result_1d))


# plotter_helicorder.wrapper(result_1d)

