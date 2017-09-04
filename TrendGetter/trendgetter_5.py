
# using the list of files, open each logfile into the main array

# convert the timestamps in the main array to POSIX format

# Sort the main array by timestamp oldest to newest

# using the most recent date in the main array, create  temp list of bin dates
# THis will need to take into account the number and size of bins that we want.

# for each bin interval in the list of bin timestamps
# set up a holding list
# parse thru the main array entries that fit in the interval are added to the holding list
# PERFORM WHATEVER OPERATION WE WANT, AVERAGE OR DH/DT, ETC

# convert the POSIX datetimes back to UTC.

# create the header and save the file as a CSV/JSON