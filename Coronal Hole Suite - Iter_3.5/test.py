import math

data=[
"2.3,6",
"2.4,9",
"2.5,10",
"3,8",
"3.2,7",
"2.9,9",
"4,12",
"4.5,15",
"4.3,18",
"3.8,22",
"5,19",
"5.7,20"
]

def _sum_x(xy_list):
    # the sum of x in the xy_list
    # returns a float:
    x_sum = 0

    for item in xy_list:
        datasplit = item.split(",")
        x_value = float(datasplit[0])
        x_sum = float(x_sum + x_value)
    return x_sum


def _sum_y(xy_list):
    # the sum of y in the xy_list
    # returns a float:
    y_sum = 0

    for item in xy_list:
        datasplit = item.split(",")
        y_value = float(datasplit[1])
        y_sum = float(y_sum + y_value)
    return y_sum


def _sum_x_sqr(xy_list):
    # the sum of x^2 in the xy_list
    # returns a float:
    x_sum_sq = 0

    for item in xy_list:
        datasplit = item.split(",")
        x_value = float(datasplit[0])
        x_sum_sq = float(x_sum_sq + math.pow(x_value, 2))
    return x_sum_sq


def _sum_y_sqr(xy_list):
    # the sum of y^2 in the xy_list
    # returns a float
    y_sum_sq = 0

    for item in xy_list:
        datasplit = item.split(",")
        y_value = float(datasplit[1])
        y_sum_sq = float(y_sum_sq + math.pow(y_value, 2))
    return y_sum_sq


def _sum_x_times_y(xy_list):
    # the sum of x*y in the xy_list
    # returns a float
    xy = 0
    for item in xy_list:
        datasplit = item.split(",")
        x = float(datasplit[0])
        y = float(datasplit[1])
        xy = xy + (x * y)
    return xy


def _mean_x(xy_list):
    # the mean of the x values in the xy_list
    # retruns a float
    x_sum = _sum_x(xy_list)
    x_count = float(len(xy_list))
    x_mean = float(x_sum / x_count)
    return x_mean


def _mean_y(xy_list):
    # the mean of the y values in the xy_list
    # retruns a float
    y_sum = _sum_y(xy_list)
    y_count = float(len(xy_list))
    y_mean = float(y_sum / y_count)
    return y_mean


# ################################################################
# Regression Analysis
# ################################################################
def _regression_analysis(CH_data):
    xy_data = CH_data
    sm_x = _sum_x(xy_data)
    sm_y = _sum_y(xy_data)
    sm_x_sqr = _sum_x_sqr(xy_data)
    sm_y_sqr = _sum_y_sqr(xy_data)
    sm_x_times_y = _sum_x_times_y(xy_data)
    mn_x = _mean_x(xy_data)
    mn_y = _mean_y(xy_data)
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
    report_string = ("<br>Linear approximation is: Predicted windspeed = " + str(rg_a)[:6] + " + " + str(rg_b)[:6] + " * coronal hole area on meridian     <br>Pearsons correlation |r| = " + str(pearson_r_value)[:6] + "\n")
    print(report_string)
    return regression_parameters


print(_regression_analysis(data))