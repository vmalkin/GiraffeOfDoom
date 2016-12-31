import time
import datetime
import math

def sunriseset(day_number):
   # This function starts at the summer solstice, so correct the day number as supplied to deal with this
   solstice_offset = 11

   # twStart, sunrise, sunset, twEnd
   summer_values = (3.0, 4.7167, 21.4833, 23.1667)
   winter_diffs = (3.5167, 2.6167, -4.4833, -5.3667)

   # Daylight Savings, SHOULD be last Sunday of Sept, first Sunday of April
   dst_start = 237 + solstice_offset
   dst_end = 91 + solstice_offset

   # Correct the day number, as this function works on a solar year from summer solstice, to summer solstice
   if day_number < 11:
       day_number = 365 - day_number
   else:
       day_number = day_number - solstice_offset

   # Prepare return array.
   t_riseset_array = []

   # The year number is converted into a format for the sin function. The curve of sunrise/set follows this sine curve
   yearpoint = (1.0 / 365.0) * day_number * math.pi
   yearpoint = math.sin(yearpoint)
   # print("yearpoint is " + str(yearpoint))

   # we are using half curve of a sin wave function to approximate the curve of rising and setting for the year
   for i in range (0,4):
       t_winter = yearpoint * winter_diffs[i]
       hourvalue = summer_values[i] + t_winter
       # print("hourvalue is " + str(hourvalue))
       t_riseset_array.append(hourvalue)

   # if it's daylight savings, we need to add an hour.
   if day_number > dst_start or day_number < dst_end:
       temparray = []
       for item in t_riseset_array:
           datavalue = item + 1
           temparray.append(datavalue)

       t_riseset_array = temparray

   # # We need to correct any hour values that have gone beyond 24
   # temparray = []
   # for hour in t_riseset_array:
   #     if hour > 24:
   #         hour = hour - 24
   #     temparray.append(hour)
   #
   # t_riseset_array = temparray

   return t_riseset_array


def set_exposure():
   dt = datetime.datetime.now()
   day_of_year = datetime.datetime.now().timetuple().tm_yday
   nowhour = float(dt.strftime('%H'))
   nowmin = float(dt.strftime('%M'))
   nowtime = float(nowhour + (nowmin/60))

   nowtime = 5

   print("time is " + str(nowtime))

   EXPOSURE_DAY = 0.00008
   EXPOSURE_NIGHT = 30
   CENT_EXPOSURE_INTERVAL = (EXPOSURE_DAY - EXPOSURE_NIGHT) / 100

   return_exposure = 0

   # get datetime array for sunrise and sunset values
   datetime_array = sunriseset(day_of_year)
   print(datetime_array)

   # Morning twilight period?
   if nowtime > float(datetime_array[0]) and nowtime <= float(datetime_array[1]):
       print("Morning twilight exposure")
       cent_time_interval = (datetime_array[1] - datetime_array[0]) / 100
       return_exposure = ((nowtime - datetime_array[1]) / cent_time_interval) * CENT_EXPOSURE_INTERVAL

   # is it daytime?
   if nowtime > float(datetime_array[1]) and nowtime <= float(datetime_array[2]):
       print("Daytime exposure")
       return_exposure = EXPOSURE_DAY

   # Finally, evening twilight period?
   if nowtime > float(datetime_array[2]) and nowtime <= (float(datetime_array[3])):
       print("Evening twilight exposure")
       cent_time_interval = (datetime_array[3] - datetime_array[2]) / 100
       return_exposure = ((datetime_array[2] - nowtime) / cent_time_interval) * CENT_EXPOSURE_INTERVAL

   # is it nighttime?
   if nowtime > 0 and nowtime <= float(datetime_array[0]):
       print("Nighttime exposure - after midnight")
       return_exposure = EXPOSURE_NIGHT
   if (nowtime > float(datetime_array[3]) and nowtime <= 0):
       print("Nighttime exposure - before midnight")
       return_exposure = EXPOSURE_NIGHT

   return float(return_exposure)

print(set_exposure())