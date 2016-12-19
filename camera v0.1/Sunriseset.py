import math

# This function returns the rising and setting times of the sun
# based on the day number in question, time of summer rise/set, and the offset of winter rise/set
# these values (and decimal equivs) are:
# 0300 (3), 0543 (5.72), 2149 (21.48), 2410 (24.17) - twilight, sunrise, sunset, twilight, SUMMER
# 0631 (6.52), 0820 (8.33), 1700, (17), 1848 (18.8) - twilight, sunrise, sunset, twilight, WINTER
# 3.52, 2.62, -4.48, -5.37 - twilight, sunrise, sunset, twilight, WINTER DIFFS

# from datetime import datetime
# day_of_year = datetime.now().timetuple().tm_yday

def sunriseset(day_number, riseset_value, t_summer_asdecimal, t_winter_diff_asdecimal):
    # This function starts at the summer solstice, so correct the day number as supplied to deal with this
    solstice_offset = 11
    if day_number < 11:
        day_number = 365 - day_number
    else:
        day_number = day_number - solstice_offset

    if riseset_value == "rise":
        signcorrection = 1
    else:
        signcorrection = -1

    # we are using half curve of a sin wave function to approximate the curve of rising and setting for the year
    yearpoint = math.sin((1/365)*day_number*math.pi)
    t_winter_asdecimal = (t_winter_diff_asdecimal + yearpoint) * signcorrection
    t_riseset = t_summer_asdecimal + t_winter_asdecimal










