import datapoint
import forecast as fc
import main
from decimal import *

CH_data = main.load_datapoints("log.csv")

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
    coverage = fc.CH_match_launchdate(CH_data, item[0])
    date = float(item[0])
    windspeed = item[1]
    appenditem = str(date) + "," + str(coverage) + "," + str(windspeed)
    coverage_data.append(appenditem)

# print(fc.CH_match_launchdate(CH_data, 1522695859.073293))


with open ("testscatter.csv", 'w') as w:
    for item in coverage_data:
        w.write(str(item) + '\n')


# This will create the parameters for a linear model:
# y = rg_a + rg_b * x
parameters = fc.regression_analysis(coverage_data)
rg_a = Decimal(parameters[0])
rg_b = Decimal(parameters[1])
pearson = Decimal(parameters[2])
print("Linear approximation is: y = " + str(rg_a)[:6] + " + " + str(rg_b)[:6] + " * x     R = " + str(pearson)[:6])

# the array that will hold prediction values
prediction_array = []

for item in CH_data:
    predict_speed = rg_a + (rg_b * Decimal(item.coronal_hole_coverage))
    # predict_speed = Decimal(predict_speed)
    transittime = fc.ASTRONOMICAL_UNIT_KM / predict_speed
    # transittime = Decimal(transittime)
    futurearrival = float(item.posix_date) + float(transittime)
    futurearrival = fc.posix2utc(futurearrival)
    prediction = str(futurearrival) + "," + str(predict_speed)
    prediction_array.append(prediction)

avg = 0
for item in CH_data:
    avg = avg + item.wind_speed
avg_speed = avg / len(CH_data)
delay_days = (fc.ASTRONOMICAL_UNIT_KM / avg_speed) / (60*60*24)
print("Average Windspeed is " + str(avg_speed)[:6] + "km/s")
print("Coronal Hole effects will be felt in " + str(delay_days)[:3] + " days")


with open ("prediction.csv", 'w') as w:
    for item in prediction_array:
        w.write(str(item) + '\n')
