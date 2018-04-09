# This will contain the forecasting algorithm
ASTRONOMICAL_UNIT_KM = 149597900
import math
import time
from decimal import *

# convert the internal posx_date to UTC format
def posix2utc(posix_date):
    utctime = time.gmtime(int(float(posix_date)))
    utctime = time.strftime('%Y-%m-%d %H:%M:%S', utctime)
    return utctime

# Parse CH coverage the matches the launchdate - return the CH coverage
# CHData uses a datapoint object to store it's information
def CH_match_launchdate(CHData, launchdate):
    chcover = 0
    for i in range(1, len(CHData)):
        topvalue = int(CHData[i].posix_date)
        lowervalue = int(CHData[i - 1].posix_date)
        launchdate = int(launchdate)

        if launchdate <= topvalue and  launchdate > lowervalue:
            chcover = CHData[i].coronal_hole_coverage

    return chcover


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


def regression_analysis(CH_data):
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

    sxx = sm_x_sqr - (1 / count_n) * math.pow(sm_x, 2)
    syy = sm_y_sqr - (1 / count_n) * math.pow(sm_y, 2)
    sxy = sm_x_times_y - (1 / count_n) * sm_x * sm_y

    # calculate the a and b values needed for the regression formula
    # y = rg_a + rg_b * x
    rg_b = float(sxy / sxx)
    rg_a = float(mn_y - (rg_b * mn_x))
    pearson_r_value = math.sqrt(math.pow((sxy / math.sqrt(sxx * syy)), 2))

    regression_parameters = [rg_a, rg_b, pearson_r_value]

    return regression_parameters


# # ################################################################
# # C A L L   T H I S   W R A P P E R   F U N C T I O N
# # ################################################################
def calculate_forecast(CH_data):
    # load in the test data
    # parse the data to find the CH date that matches the speed of solar wind
    revised_ch_data = []

    getcontext().prec = 6

    # This part corresponds to forecast.calculate_forecast()
    # the revised data list is NOT a list of objects, but data.
    revised_ch_data = []

    # get the launchdate for each datapoints windspeed
    for data_p in CH_data:
        appenddata = []
        appenddata.append(data_p.launch_date)
        appenddata.append(data_p.wind_speed)
        revised_ch_data.append(appenddata)

    # get the coverage for the launch time
    coverage_data = []

    for item in revised_ch_data:
        coverage = CH_match_launchdate(CH_data, item[0])
        date = float(item[0])
        windspeed = item[1]
        appenditem = str(date) + "," + str(coverage) + "," + str(windspeed)
        coverage_data.append(appenditem)

    # print(fc.CH_match_launchdate(CH_data, 1522695859.073293))


    with open("testscatter.csv", 'w') as w:
        for item in coverage_data:
            w.write(str(item) + '\n')

    # This will create the parameters for a linear model:
    # y = rg_a + rg_b * x
    parameters = regression_analysis(coverage_data)
    rg_a = Decimal(parameters[0])
    rg_b = Decimal(parameters[1])
    pearson = Decimal(parameters[2])
    print("Linear approximation is: y = " + str(rg_a)[:6] + " + " + str(rg_b)[:6] + " * x     R = " + str(pearson)[:6])

    # the array that will hold prediction values
    prediction_array = []

    for item in CH_data:
        predict_speed = rg_a + (rg_b * Decimal(item.coronal_hole_coverage))
        # predict_speed = Decimal(predict_speed)
        transittime = ASTRONOMICAL_UNIT_KM / predict_speed
        # transittime = Decimal(transittime)
        futurearrival = float(item.posix_date) + float(transittime)
        futurearrival = posix2utc(futurearrival)
        prediction = str(futurearrival) + "," + str(predict_speed)
        prediction_array.append(prediction)

    avg = 0
    for item in CH_data:
        avg = avg + item.wind_speed
    avg_speed = avg / len(CH_data)
    delay_days = (ASTRONOMICAL_UNIT_KM / avg_speed) / (60 * 60 * 24)
    print("Average Windspeed is " + str(avg_speed)[:6] + "km/s")
    print("Coronal Hole effects will be felt in " + str(delay_days)[:3] + " days")

    with open("prediction.csv", 'w') as w:
        for item in prediction_array:
            w.write(str(item) + '\n')