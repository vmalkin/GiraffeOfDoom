"""
This code COUNTS the number of S4 events over 0.4 (40%) for the period of the passed-in query
results (typically 24 hours). The assumption is that the number of S4 events climbs during periods of activity
and wanes when things are quiet

This codes appends the count of events to an array. The median and standard deviation of this array are
returned.
"""


from statistics import mean, stdev, median
import pickle
import os
import constants as k

# Approx 3 Carrington rotations
listlength = 120000

def load_values(pickle_file):
    returnlist = []
    if os.path.exists(pickle_file) is True:
        try:
            returnlist = pickle.load(open(pickle_file, "rb"))
        except EOFError:
            print("Pickle file is empty")
    print("Loaded pickle file is " + str(len(returnlist)) + " records long")
    return returnlist


def prune_list(value_list):
    """prunes a list to a list of one - the current median value of the list"""
    medianvalue = median(value_list)
    m = []
    m.append(medianvalue)
    return m


def calc_mean(valueslist):
    """calculates the mean of a list"""
    if len(valueslist) > 2:
        return_mean = mean(valueslist)
        return_mean = round(return_mean, 5)
    else:
        return_mean = 0
    return return_mean


def calc_stdev(valueslist):
    """calculates the standard deviation of a list"""
    if len(valueslist) > 2:
        return_sigma = stdev(valueslist)
        return_sigma = round(return_sigma, 5)
    else:
        return_sigma = 0
    return return_sigma


def append_value(value_list, appendage):
    """Adds a value to a list"""
    value_list.append(appendage)
    return value_list


def save_values(save_list, pickle_file):
    pickle.dump(save_list, open(pickle_file, "wb"),0)


def count_events(valueslist):
    s4_count = 0
    for item in valueslist:
        if item[4] > 40 and item[4] <= 100:
            s4_count = s4_count + 1
    return s4_count


def wrapper(valueslist):
    # Calculate the number of s4 events from our query that meet our criteria of critical elevation
    # and not over 100%
    s4Count = count_events(valueslist)

    # Load the array of s4Counts
    s4Counts_array = load_values(k.file_count_s4)

    # append the new count to the array
    s4Counts_array.append(s4Count)

    # calculate the standard deviation of the counts
    returnvalue_mean = calc_mean(s4Counts_array)
    returnvalue_sigma = calc_stdev(s4Counts_array)

    # Periodically trim the the lists by seeding a new list with the median value of the current list
    if len(s4Counts_array) >= listlength:
        s4Counts_array = prune_list(s4Counts_array)

    # Save the array
    save_values(s4Counts_array, k.file_count_s4)

    returndict = {
        "medianvalue": returnvalue_mean,
        "mediansigma": returnvalue_sigma
    }

    print("Values: ", s4Counts_array)
    print("Mean: ", returnvalue_mean)
    print("Sigmas: ", returnvalue_sigma)

    return returndict