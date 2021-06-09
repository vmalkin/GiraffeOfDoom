"""
calulculate the mean and standard deviation of a list of numbers.
Saves each iteration of mean and stdev to a pickle file
the median value of each file is returned as a dictionary
"""

from statistics import mean, stdev, median
import pickle
import os
import constants as k

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


def wrapper(valueslist):
    # Procedure:
    # we need to purge entries where the S4 index isless than 0, and more than 100
    # We should report that these were found!
    # calculate the count of events for the time period
    s4Count = count_events(valueslist)

    totalcount = load_values(k.file_count_s4)
    s4_means = load_values(k.file_means)
    s4_sigmas = load_values(k.file_sigmas)

    # Append this count to the running list of counts
    totalcount = append_value(totalcount, s4Count)
    # calculate the mean of the counts --> append to a running list of means
    s4_means = append_value(s4_means, calc_mean(totalcount))
    # calculate he standard deviation of the counts --> append to a running list of SDs
    s4_sigmas = append_value(s4_sigmas, calc_stdev(totalcount))

    # Return the MEDIAN of the Means and Standard deviations. create the return dictionary based on this.
    returnvalue_mean = calc_median(s4_means)
    returnvalue_sigma = calc_median(s4_sigmas)

    # Periodically trim the the lists by seeding a new list with the median value from each one and starting afresh
    if len(totalcount) >= listlength:
        totalcount = prune_list(totalcount)
    if len(s4_means) >= listlength:
        s4_means = prune_list(s4_means)
    if len(s4_sigmas) >= listlength:
        s4_sigmas = prune_list(s4_sigmas)

    save_values(totalcount, k.file_count_s4)
    save_values(s4_means, k.file_means)
    save_values(s4_sigmas, k.file_sigmas)

    returndict = {
        "medianvalue": returnvalue_mean,
        "mediansigma": returnvalue_sigma
    }

    return returndict