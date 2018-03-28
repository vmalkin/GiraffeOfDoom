# This will contain the forecasting algorythm
ASTRONOMICAL_UNIT_KM = 149597900

# Get the wind speed

# calculate travel time over 1 AU
def travel_time(windspeed):
    travel_time_sec = float(ASTRONOMICAL_UNIT_KM) / float(windspeed)
    return travel_time_sec

# generate the launchdate
# The nowdate should be POSIX
def launchdate(posix_date, traveltimeseconds):
    posix_launchdate = float(posix_date) - float(traveltimeseconds)
    return posix_launchdate
    
# Store the launchdate and windspeed on the date

# Parse CH coverage the matches the launchdate
# Store the Launchdate, windspeed, CH coverage

# Calculate the Linear relationship  that produces windspeed from CH coverage

# calculate Future windspeed predictions.

# Create CSV datafile for Highcharts