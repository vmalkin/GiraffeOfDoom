import Station

# create the magnetometer stations for this run
dalmore = Station.Station("Dalmore", "Dalmore.1minbins.csv")
corstorphine = Station.Station("Corstorphine", "Corstorphine.1minbins.csv")

# init the array of stations and append
stationlist = []
stationlist.append(dalmore)
stationlist.append(corstorphine)

# print(stationlist[0].datapointarray[0].dateTime)
# print(stationlist[0].output_f[1])
# print(stationlist[1].output_f[1])

# create a list of unique timestamps based on all available times from all stations, for this run.
# make a list of all dates, duplicates and all...
temp_data = []
for magstation in stationlist:
    for i in range(0, len(magstation.output_f)):
        datasplit = magstation.output_f[i].split(",")
        testdate = datasplit[0]
        temp_data.append(testdate)

# sort the list A-Z-wise
temp_data.sort()

olddate = "2000-01-01 00:00"
date_data = []
# Go thru the temp data and write out unique datetimes only, to the final merged list.
for dateitem in temp_data:
    while dateitem != olddate:
        date_data.append(dateitem)
        olddate = dateitem

merged_data = []

# insert the headings as the first element of the merged_data[]
merged_header = "Date/Time UTC, "
for magstation in stationlist:
    merged_header = merged_header + magstation.station_name + ","

# strip off the last comma
merged_header = merged_header[:-1]
# add to merged_data array
merged_data.append(merged_header)

# Now, for each dateitem in date_data...
for dateitem in date_data:
    #  Set up a datastring. Append the date to it.
    datastring = ""
    # Go thru each magnetometer station in the station list.
    for magstation in stationlist:
        k = 0
        # check the datetime component of each entry in the output_f list
        for i in range(0, len(magstation.output_f)):
            testsplit = magstation.output_f[i].split(",")
            # if the date matches, then append the reading component to the datastring
            if dateitem == testsplit[0]:
                datastring = datastring + testsplit[1] + ","
                k = k + 1

        if k == 0:
            datastring = datastring + "0,"

    merged_data.append(dateitem + "," + datastring)
    datastring = ""

# remove final traling comma
for item in merged_data:
    item = item[:-1]

print(merged_data)