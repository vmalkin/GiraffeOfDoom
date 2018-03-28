# This will contain the forecasting algorythm
ASTRONOMICAL_UNIT_KM = 149597900
import math


# calculate travel time over 1 AU
def travel_time(windspeed):
    travel_time_sec = float(ASTRONOMICAL_UNIT_KM) / float(windspeed)
    return travel_time_sec


# generate the launchdate
# The nowdate should be POSIX
def launchdate(posix_date, traveltimeseconds):
    posix_launchdate = float(posix_date) - float(traveltimeseconds)
    return posix_launchdate


# Parse CH coverage the matches the launchdate - return the CH coverage
# that matches.
# CH Array shold be in POSIX time laready at this point. 
def CH_match_launchdate(ch_array, posix_launchdate):
    # What we want to do is find the timestamp in the CH array that is the
    # closest to the supplied launchdate. 
    # data is of format posixtime, ch_coverage, wind_speed, wind_density
    delta_smallest = 1000000000
    return_ch_coverage = 0
    for item in ch_array:
        datasplit = item.split(",")
        checktime = datasplit[0]  # posix date
        ch_coverage = datasplit[1]
        delta_current = math.sqrt(math.pow((checktime - posix_launchdate),2))
        if delta_current < delta_smallest:
            return_ch_coverage = ch_coverage
    return return_ch_coverage

# Store the Launchdate, windspeed, CH coverage

# Calculate the Linear relationship  that produces windspeed from CH coverage

# calculate Future windspeed predictions.

# Create CSV datafile for Highcharts
    
