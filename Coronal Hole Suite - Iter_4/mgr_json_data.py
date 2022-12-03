import requests
import time
import datetime
import common_data

WIND_SPEED_THRESHOLD = 800
NULL = ""


wind_density = 0
wind_speed = 0
satdata = []

def _utc2posix(timestamp):
    # 2018-03-19 02:05:00.000
    # %Y-%m-%d %H:%M:%S
    posix_time = time.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    posix_time = time.mktime(posix_time)
    return posix_time


def _get_json(data_url):
    # DISCOVR satellite data in JSON format
    # first is the header values, then the data values:
    # ["time_tag","density","speed","temperature"]
    # ["2018-03-19 02:05:00.000","6.35","573.4","330513"]
    try:
        url = data_url
        response = requests.get(url)
        discovr_data = response.json()  # requests has built in json
    except:
        # time_now = str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        discovr_data = "no_data"
    return discovr_data


def _parse_json_convert_time(jsonfile):
    # converts the time to POSIX
    # grabs the Plasma and Density data
    # returns a python list
    returnlist = []
    for i in range(1, len(jsonfile)):
        date_posix = _utc2posix(jsonfile[i][0])
        wind_density = jsonfile[i][1]
        wind_speed = jsonfile[i][2]

        csvdata = str(date_posix) + "," + str(wind_density) + "," + str(wind_speed)
        returnlist.append(csvdata)

    return returnlist


def _parse_json_prune(posix_list):
    # we want only the data for the last hour.
    # we will return a modified array of the current data only
    nowtime = _utc2posix(str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")))
    prevtime = nowtime - 3600  # the past hour
    returnarray = []

    for i in range (1, len(posix_list)):
        datasplit = posix_list[i].split(",")
        checkdate = datasplit[0]
        wind_density = datasplit[1]
        wind_speed = datasplit[2]
        # print(str(checkdate) + " " + str(nowtime) + " " + str(prevtime))
        if float(checkdate) > float(str(prevtime)) and float(checkdate) <= float(str(nowtime)):
            csvdata = str(checkdate) + "," + str(wind_density) + "," + str(wind_speed)
            returnarray.append(csvdata)
    return returnarray


def _plasma_density(posix_list):
    try:
        wind_density = 0
        counter = 0
        for i in range(1, len(posix_list)):
            datasplit = posix_list[i].split(",")
            value = datasplit[1]
            wind_density = wind_density + value
            counter = counter + 1

        wind_density = wind_density / counter
    except:
        wind_density = 0
    return wind_density


def _plasma_speed(posix_list):
    try:
        wind_speed = 0
        counter = 0
        for i in range(1, len(posix_list)):
            datasplit = posix_list[i].split(",")
            value = datasplit[2]
            wind_speed = wind_speed + value
            counter = counter + 1
        wind_speed = wind_speed / counter

        if wind_speed > WIND_SPEED_THRESHOLD:
            wind_speed = 400
    except:
        wind_speed = 0
    return wind_speed


# ################################
# W R A P P E R   F U N C T I O N
# ################################
def wrapper(dataurl):
    satdata = _get_json(dataurl)
    if satdata == "no_data":
        # Unable to get DISCOVR data
        common_data.report_string = common_data.report_string + "DISCOVR does not have new solar wind data to report \n"
        wind_density = 0
        wind_speed = 0
    else:
        for item in satdata:
            print(item)
        # # parse new data to the correct format
        # # The timestampt is in POSIX format
        # dscvr_data = _parse_json_convert_time(satdata)
        #
        # # we want only the last hour of data
        # dscvr_data = _parse_json_prune(dscvr_data)
        #
        # # get the avg windspeed and plasma density
        # wind_density = _plasma_density(dscvr_data)
        # wind_speed = _plasma_speed(dscvr_data)
    return None
