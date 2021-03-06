def test_regression_constants():
    import forecast

    tree = []
    tree.append("a,4,0.8")
    tree.append("a,8,1")
    tree.append("a,8,3")
    tree.append("a,10,3.5")
    tree.append("a,13,3.5")
    tree.append("a,16,4.5")
    tree.append("a,20,5.5")
    tree.append("a,23,4.7")
    tree.append("a,28,6")
    tree.append("a,30,6")
    tree.append("a,33,8")
    tree.append("a,35,7")
    tree.append("a,38,7")
    tree.append("a,42,7.5")

    # a and B should be 1.0842 and 0.1715
    forecast.calculate_forecast(tree)

# def test_datetime_shift():
#     import forecast
#     # load in the test data
#     filename = "testdata.csv"
#     CH_data = []
#     with open(filename, 'r') as f:
#         for line in f:
#             line = line.strip()  # remove \n from EOL
#             CH_data.append(line)
#
#     # parse the data to find the CH date that matches the speed of solar wind
#     revised_ch_data = []
#
#     for item in CH_data:
#         datasplit = item.split(",")
#         chdate = datasplit[0]
#         current_ch = datasplit[1]
#         windspeed = datasplit[2]
#
#         # what is the tranist time for the current windspeed @ 1AU
#         transittime = forecast.travel_time(windspeed)
#
#         # calculate when the wind left the sun
#         launchtime = forecast.launchdate(chdate, transittime)
#
#         # whats was the actual CH coverage on that day?
#         reviseCHcover = forecast.CH_match_launchdate(CH_data, launchtime)
#
#         # Collate the revised launchdate with the actual speed of the solar wind
#         # append to revised datalist
#         # newdata = chdate + "," + current_ch + "," + str(launchtime) + "," + reviseCHcover + "," + windspeed
#         newdata = str(launchtime) + "," + reviseCHcover + "," + windspeed
#         revised_ch_data.append(newdata)
#
#     with open ("TESTSAVED.CSV", 'w') as w:
#         for item in revised_ch_data:
#             w.write(str(item) + '\n')
#
#     for item in CH_data:
#         print(item)
#
#     # This will create the parameters for a linear model:
#     # y = rg_a + rg_b * x
#     parameters = forecast.regression_analysis(revised_ch_data)
#     rg_a = parameters[0]
#     rg_b = parameters[1]
#     pearson = parameters[2]
#
#     # the array that will hold prediction values
#     prediction_array = []
#
#
#     for item in CH_data:
#         datasplit = item.split(",")
#         launchdate = datasplit[0]
#         coronal_hole_opening = datasplit[1]
#         windspeed = datasplit[2]
#
#         predict_speed = float(rg_a) + float(rg_b) * float(coronal_hole_opening)
#         transittime = forecast.ASTRONOMICAL_UNIT_KM / predict_speed
#         arrivaldate = float(launchdate) + float(transittime)
#
#         prediction = str(arrivaldate) + "," + str(windspeed)
#
#         prediction_array.append(prediction)
#
#     with open ("prediction.csv", 'w') as w:
#         for item in prediction_array:
#             w.write(str(item) + '\n')


def test_datetime_shift():
    import datapoint as dp
    import forecast_v2 as forecast

    # load in the test data
    filename = "testdata.csv"
    CH_data = []

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()  # remove \n from EOL
            datasplit = line.split(",")
            posixdate = datasplit[0]
            ch = datasplit[1]
            speed = datasplit[2]
            density = datasplit[3]
            dataitem = dp.DataPoint(posixdate, ch, speed, density)
            CH_data.append(dataitem)

    # #####################################################################################################
    # Test that we have enough data to start making the predictions.
    # Else return notification as to how long before predictions can start
    # #####################################################################################################

    # parse the data to find the CH date that matches the speed of solar wind
    revised_ch_data = []

    for data_p in CH_data:
        # Each datapoint can report it's speed, and the launch date of the space weather
        # we need to find the CH coverage for the date in question.

        # whats was the actual CH coverage on that day?
        reviseCHcover = forecast.CH_match_launchdate(CH_data, data_p.launch_date )

        # Collate the revised launchdate with the actual speed of the solar wind
        # append to revised datalist
        # newdata = chdate + "," + current_ch + "," + str(launchtime) + "," + reviseCHcover + "," + windspeed
        newdata = str(data_p.launch_date) + "," + reviseCHcover + "," + data_p.wind_speed
        revised_ch_data.append(newdata)


    # This will create the parameters for a linear model:
    # y = rg_a + rg_b * x
    parameters = forecast.regression_analysis(revised_ch_data)
    rg_a = parameters[0]
    rg_b = parameters[1]
    pearson = parameters[2]

    # the array that will hold prediction values
    prediction_array = []


    for item in CH_data:
        predict_speed = float(rg_a) + float(rg_b) * float(item.coronal_hole_coverage)
        transittime = forecast.ASTRONOMICAL_UNIT_KM / predict_speed
        arrivaldate = float(item.launch_date) + float(transittime)

        prediction = str(arrivaldate) + "," + str(predict_speed)

        prediction_array.append(prediction)

    with open ("prediction.csv", 'w') as w:
        for item in prediction_array:
            w.write(str(item) + '\n')



test_datetime_shift()
