# datapoint class to help manage some of the nonsense!
#
# posix_date - the date that corresponds to the current CH reading (posix compliant date)
# coronal_hole_coverage - the coverage at the date (a percentage between 0-1)
# wind_speed - windspeed at the time of posix_date as recorded by DISCOVR (km/s)
# wind_density - wind density at the time of posix_date as recorded by DISCOVR (particles/m^3)
#


class datapoint:
    def __init__(self, posix_date, coronal_hole_coverage, wind_speed, wind_density):
        self.ASTRONOMICAL_UNIT_KM = 149597900
        self.posix_date = posix_date
        self.coronal_hole_coverage = coronal_hole_coverage
        self.wind_speed = wind_speed
        self.wind_density = wind_density

        # A datapoint can also calculate the corrected launchtime of the current wind data, knowing the speed
        # and the size of an astronomical unit
        self.launch_date = float(self.posix_date) - float(self.travel_time())

    # calculate travel time over 1 AU
    def travel_time(self):
        if self.wind_speed == 0:
            reportedspeed = 400
        else:
            reportedspeed = self.wind_speed

        travel_time_sec = float(self.ASTRONOMICAL_UNIT_KM) / float(reportedspeed)

        return travel_time_sec

