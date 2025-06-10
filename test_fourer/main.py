from scipy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt
import numpy as np
# from decimal import Decimal, getcontext, ROUND_DOWN
# getcontext().prec = 4
import os

def try_create_directory(directory):
    if os.path.isdir(directory) is False:
        print("Creating image file directory...")
        try:
            os.makedirs(directory)
            print("Directory created.")
        except:
            if not os.path.isdir(directory):
                print("Unable to create directory")

def make_decimal(string_value):
    result = 0
    try:
        result = float(string_value)
        result = round(result, 4)
    except ValueError:
        print("ERROR - string is not a number.")
    return result

csv_data = []

img_dir = "images"
movie_dir = "movies"
try_create_directory(img_dir)
try_create_directory(movie_dir)

with open("dr01_24hr.csv", "r") as c:
    for line in c:
        l = line.strip()
        l = l.split(",")
        string_data = l[1]

        # this is weird, why do we need to add 100 here?
        decimal_data = make_decimal(string_data) + 100
        csv_data.append(decimal_data)

# The number of samples to do the FFT for. Part of a subset of the full date
sample_period = 1800

if len(csv_data) > sample_period:
    sample_data = []
    for i in range(0, len(csv_data)):
        # Build up the sub-sample array from the main data
        sample_data.append(csv_data[i])

        # Once our sub sample has reached the appropriate size, pop the oldest value
        # and do FFT analysis
        if len(sample_data) == sample_period:
            sample_data.pop(0)
            progress = round((i / len(csv_data)), 3)
            print("Progress: ", progress)
            # hertz
            sample_rate = 0.5
            # duration in seconds
            duration = len(sample_data) * (1 / sample_rate)

            # Number of samples in normalized_tone
            N = int(sample_rate * duration)

            # the FFT calculation and visualisation
            norms = []
            for item in sample_data:
                dd = (item / max(sample_data))
                # print(item, max(csv_data))
                normalized_tone = np.int16(dd * 32767)
                norms.append(normalized_tone)

            yf = rfft(norms)
            xf = rfftfreq(N, 1 / sample_rate)
            # print(yf)
            fig, ax = plt.subplots(layout="constrained", figsize=(4, 4), dpi=200)
            plt.plot(xf, np.abs(yf))
            ax.set_ylim([0, 100000])
            ax.set_xlim([0, 0.05])
            plotfilename = img_dir + os.sep + str(i) + ".jpg"
            # print(plotfilename)
            plt.savefig(plotfilename)
            plt.close("all")


