# This will contain the forecasting algorithm
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
    return_index = -1

    for i in range(0, len(ch_array)):
        datasplit = ch_array[i].split
        chdate = datasplit[0]

        # test the date to see if it is closest
        delta_check = math.sqrt(math.pow((posix_launchdate - chdate),2))
        if delta_check < delta_smallest:
            return_index = i
    
    returnsplit = ch_array[return_index].split(",")
    
    # the CH coverage should be the second value in the split
    ch_coverage = returnsplit[1]
    
    return ch_coverage

# Store the Launchdate, windspeed, CH coverage

# ################################################################
# Functions required for the Linear Regression 
# taken from "A First Course in applied stats" by Clark and Randal
# ISBN 978-1-4425-4151-1
# Pg 70
# ################################################################
def reduce_chdata(ch_data):
    #must be run first
    # reduces CH list to just x and y values, strips dates, etc
    returndata = []
    
    # data is in format a,b,c - we want only b,c
    for item in ch_data:
        datasplit = item.split(",")
        returnitem = datasplit[1] + "," + datasplit[2]
        returndata.append(returnitem)
    return returndata

def sum_x(xy_list):
    # the sum of x in the xy_list
    # returns a float:
    x_sum = 0
    
    for item in xy_list:
        datasplit = item.split(",")
        x_value = float(datasplit[0])
        x_sum = float(x_sum + x_value)
    return x_sum

def sum_y(xy_list):
    # the sum of y in the xy_list
    # returns a float:
    y_sum = 0
    
    for item in xy_list:
        datasplit = item.split(",")
        y_value = float(datasplit[1])
        y_sum = float(y_sum + y_value)
    return y_sum

def sum_x_sqr(xy_list):
    # the sum of x^2 in the xy_list
    # returns a float:
    x_sum_sq = 0
    
    for item in xy_list:
        datasplit = item.split(",")
        x_value = float(datasplit[0])
        x_sum_sq = float(x_sum_sq + math.pow(x_value, 2))
    return x_sum_sq    

def sum_y_sqr(xy_list):
    # the sum of y^2 in the xy_list
    # returns a float
    y_sum_sq = 0
    
    for item in xy_list:
        datasplit = item.split(",")
        y_value = float(datasplit[1])
        y_sum_sq = float(y_sum_sq + math.pow(y_value, 2))
    return y_sum_sq

def sum_x_times_y(xy_list):
    # the sum of x*y in the xy_list
    # returns a float
    xy = 0
    for item in xy_list:
        datasplit = item.split(",")
        x = float(datasplit[0])
        y = float(datasplit[1])
        xy = xy + (x * y)
    return xy


def mean_x(xy_list):
    # the mean of the x values in the xy_list
    # retruns a float
    x_sum = sum_x(xy_list)
    x_count = float(len(xy_list))
    x_mean = float(x_sum / x_count)
    return x_mean

def mean_y(xy_list):
    # the mean of the y values in the xy_list
    # retruns a float
    y_sum = sum_y(xy_list)
    y_count = float(len(xy_list))
    y_mean = float(y_sum / y_count)
    return y_mean

   
# ################################################################
# C A L L   T H I S   W R A P P E R   F U N C T I O N  
# ################################################################
def calculate_forecast(CH_data):
    # Match the current CH reading with the earlier launchdate, based on CH wind speed.
    # Build a new list of these corrected values.
    # timevalues are in POSIX format
    xy_data = []
    
    for item in CH_data:
        datasplit = item.split(",")
        chdate = datasplit[0]
        windspeed = datasplit[1]
        winddensity = datasplit[2]
        transittime = travel_time(windspeed)
        launchtime = launchdate(chdate, transittime)
        reviseCHcover = CH_match_launchdate(CH_data, launchdate)
        
        newdata = launchtime + "," + reviseCHcover + "," + windspeed
        xy_data.append(newdata)
        
    
    # reduce the CH data to x y values only
    xy_data = reduce_chdata(CH_data)
    
    # ################################################################
    # Regression Analysis
    # ################################################################
    sm_x = sum_x(xy_data)
    sm_y = sum_y(xy_data)
    sm_x_sqr = sum_x_sqr(xy_data)
    sm_y_sqr = sum_y_sqr(xy_data)
    sm_x_times_y = sum_x_times_y(xy_data)  
    mn_x = mean_x(xy_data)
    mn_y = mean_y(xy_data)
    count_n = len(xy_data)

    sxx = sm_x_sqr - (1/count_n) * math.pow(sm_x, 2)
    syy = sm_y_sqr - (1/count_n) * math.pow(sm_y, 2)
    sxy = sm_x_times_y - (1/count_n) * sm_x * sm_y
    
    # calculate the a and b values needed for the regression formula
    # y = rg_a + rg_b * x
    rg_b = float(sxy / sxx)
    rg_a = float(mn_y - (rg_b * mn_x))
    pearson_r_value = math.sqrt(math.pow((sxy / math.sqrt(sxx * syy)),2))
    
    print(str(sxx) + " " + str(syy) + " " + str(sxy))
    print(str(rg_a) + " " + str(rg_b) + " " + str(pearson_r_value))
    
    