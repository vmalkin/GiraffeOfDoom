import scipy
import matplotlib
import numpy as np
# from decimal import Decimal, getcontext, ROUND_DOWN
# getcontext().prec = 4

def make_decimal(string_value):
    result = np.nan
    try:
        result = float(string_value)
        result = round(result, 4)
    except ValueError:
        print("ERROR - string is not a number.")
    return result

csv_data = []

with open("dr01_24hr.csv", "r") as c:
    for line in c:
        l = line.strip()
        l = l.split(",")
        string_data = l[1]
        decimal_data = make_decimal(string_data)
        print(decimal_data)
        csv_data.append(decimal_data)


