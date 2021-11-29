from statistics import median

def filter_median(item_list):
    """
    Takes in a list of DataPoints and performs a median filter on the list. The list is truncated at the start
    and end by one halfwindow
    """

    # Full window = halfwindow * 2 + 1
    halfwindow = 1
    returnlist = []

    for i in range(halfwindow, len(item_list) - halfwindow):
        data_store = []
        for j in range(0 - halfwindow, halfwindow + 1):
            data_store.append(item_list[i + j])

        print(data_store)

        medianvalue = median(data_store)
        returnlist.append(medianvalue)
    return returnlist

l = [1,2,3,2,3,4,3,56,2,3,23,1,2,3,4,3,2]
print(filter_median(l))