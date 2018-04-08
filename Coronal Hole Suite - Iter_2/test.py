import datapoint
import forecast as fc
import main


CH_data = main.load_datapoints("log.csv")


# This part corresponds to forecast.calculate_forecast()
# the revised data list is NOT a list of objects, but data.
revised_ch_data = []

# get the launchdate for each datapoints windspeed
for data_p in CH_data:
    appenddata = []
    appenddata.append(data_p.launch_date)
    appenddata.append(data_p.wind_speed)
    revised_ch_data.append(appenddata)

## Sort the list by launchdate - there will be some shifting of the datapoints.
sorted = []
for i in range(0, len(revised_ch_data)):
    
    

# Save a list to a disc file
csvlist = revised_ch_data
with open("testsaveddata.csv", 'w') as w:
    for item in csvlist:
        w.write(str(item) + '\n')

# # This will create the parameters for a linear model:
# # y = rg_a + rg_b * x
# parameters = regression_analysis(revised_ch_data)
# rg_a = parameters[0]
# rg_b = parameters[1]
# pearson = parameters[2]
# print("Linear approximation is: y = " + str(rg_a) + " + " + str(rg_b) + " * x     R = " + str(pearson))
#
# # the array that will hold prediction values
# prediction_array = []
#
#
# for item in CH_data:
#     predict_speed = float(rg_a) + (float(rg_b) * float(item.coronal_hole_coverage))
#     transittime = ASTRONOMICAL_UNIT_KM / predict_speed
#     futurearrival = float(item.launch_date) + float(transittime)
#     futurearrival = posix2utc(futurearrival)
#     prediction = str(futurearrival) + "," + str(predict_speed)
#
#     prediction_array.append(prediction)
#
# with open ("prediction.csv", 'w') as w:
#     for item in prediction_array:
#         w.write(str(item) + '\n')
