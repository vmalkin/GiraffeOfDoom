import main_v5 as m
import time

resultlist = m.parse_database()

m.create_s4_sigmas(resultlist, "test_stddev.csv")
#
# posix_time = int(time.time())
# # We recycle the create_sigmas function to generate a 24hr CSV logfile
# dt = m.posix2utc(posix_time).split(" ")
# name = dt[0] + ".csv"
# filepath = m.logfiles + "/" + name
# m.create_s4_sigmas(resultlist, filepath)
