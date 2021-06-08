"""
calulculate the mean and standard deviation of a list of numbers.
Saves each iteration of mean and stdev to a pickle file
the median value of each file is returned as a dictionary
"""

from statistics import mean, stdev, median
import pickle
import os

listlength = 7000


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
    medianvalue = calc_median(value_list)
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


def calc_median(value_list):
    """Calculate and return the median value of a list"""
    if len(value_list) > 2:
        return_median = median(value_list)
        return_median = round(return_median, 5)
    else:
        return_median = 0
    return return_median


def count_events(valueslist):
    s4_count = 0
    for item in valueslist:
        if item[4] > 40 and item[4] <= 100:
            s4_count = s4_count + 1
    return s4_count


def wrapper(valueslist, pickle_count_file):
    # we need to purge entries where the S4 index isless than 0, and more than 100
    # We should report that these were found!
    s4Count = count_events(valueslist)
    totalcount = load_values(pickle_count_file)


    if len(totalcount) >= listlength:
        totalcount = prune_list(totalcount)

    totalcount = append_value(totalcount, s4Count)

    save_values(totalcount, pickle_count_file)

    s4_mean = calc_median(totalcount)
    s4_sigma = calc_stdev(totalcount)

    returndict = {
        "medianvalue": s4_mean,
        "mediansigma": s4_sigma
    }

    return returndict