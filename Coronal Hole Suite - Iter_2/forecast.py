# This will contain the forecasting algorithm
ASTRONOMICAL_UNIT_KM = 149597900
import math
import time

# convert the internal posx_date to UTC format
def posix2utc(posix_date):
    utctime = time.gmtime(int(float(posix_date)))
    utctime = time.strftime('%Y-%m-%d %H:%M:%S', utctime)
    return utctime

# Parse CH coverage the matches the launchdate - return the CH coverage
def CH_match_launchdate(ch_array, posix_launchdate):
    # What we want to do is find the timestamp in the CH array that is the
    # closest to the supplied launchdate. 
    # data is of format posixtime, ch_coverage, wind_speed, wind_density
    delta_smallest = 1000000000
    return_index = -1

    for i in range(0, len(ch_array)-1):
        chdate = ch_array[i].posix_date

        # test the date to see if it is closest
        delta_check = math.sqrt(math.pow((float(posix_launchdate) - float(chdate)),2))
        if delta_check < delta_smallest and delta_check < 3600:
            delta_smallest = delta_check
            return_index = i
    
    # Using the result for the closest date match, grab the index from that date 
    # and return the coverage figure
    ch_coverage= ch_array[return_index].coronal_hole_coverage

    return ch_coverage


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

    for data_p in CH_data:
        # Each datapoint can report it's speed, and the launch date of the space weather
        # we need to find the CH coverage for the date in question.

        # whats was the actual CH coverage on that day?
        reviseCHcover = CH_match_launchdate(CH_data, str(data_p.launch_date))

        # Collate the revised launchdate with the actual speed of the solar wind
        # append to revised datalist
        # newdata = chdate + "," + current_ch + "," + str(launchtime) + "," + reviseCHcover + "," + windspeed
        newdata = str(data_p.launch_date) + "," + str(reviseCHcover) + "," + str(data_p.wind_speed)
        revised_ch_data.append(newdata)


    # This will create the parameters for a linear model:
    # y = rg_a + rg_b * x
    parameters = regression_analysis(revised_ch_data)
    rg_a = parameters[0]
    rg_b = parameters[1]
    pearson = parameters[2]
    print("Linear approximation is: y = " + str(rg_a) + " + " + str(rg_b) + " * x     R = " + str(pearson))

    # the array that will hold prediction values
    prediction_array = []


    for item in CH_data:
        predict_speed = float(rg_a) + (float(rg_b) * float(item.coronal_hole_coverage))
        transittime = ASTRONOMICAL_UNIT_KM / predict_speed
        futurearrival = float(item.launch_date) + float(transittime)
        futurearrival = posix2utc(futurearrival)
        prediction = str(futurearrival) + "," + str(predict_speed)

        prediction_array.append(prediction)

    with open ("prediction.csv", 'w') as w:
        for item in prediction_array:
            w.write(str(item) + '\n')

    