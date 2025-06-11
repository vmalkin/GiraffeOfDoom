from scipy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt
import numpy as np
# from decimal import Decimal, getcontext, ROUND_DOWN
# getcontext().prec = 4
import os
import time
import multiprocessing

number_cores = 10
sample_period = 1800
# hertz
sample_rate = 0.5
img_dir = "images"
movie_dir = "movies"

t_start = time.time()

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

def process_fft_visualisation(data_to_process, process_number):
    print("Multitasking Process started: ", process_number)
    # The number of samples to do the FFT for. Part of a subset of the full date
    sample_data = []
    for i in range(0, len(data_to_process)):
        # Build up the sub-sample array from the main data
        sample_data.append(data_to_process[i])

        # Once our sub sample has reached the appropriate size, pop the oldest value
        # and do FFT analysis
        if len(sample_data) == sample_period:
            sample_data.pop(0)
            progress = round((i / len(data_to_process)), 3)
            print("Progress: ", process_number, progress)

            # duration in seconds
            duration = len(sample_data) * (1 / sample_rate)

            # Number of samples in normalized_tone
            N = int(sample_rate * duration)

            # the FFT calculation
            norms = []
            for item in sample_data:
                dd = (item / max(sample_data))
                # print(item, max(csv_data))
                normalized_tone = np.int16(dd * 32767)
                norms.append(normalized_tone)
            yf = rfft(norms)
            xf = rfftfreq(N, 1 / sample_rate)

            # The visualisation
            fig, ax = plt.subplots(layout="constrained", figsize=(8, 4), dpi=200)
            plt.plot(xf, np.abs(yf))
            ax.set_ylim([100, 10000000])
            ax.set_xlim([0, 0.05])
            plt.yscale("log")
            plotfilename = img_dir + os.sep + str(process_number) + "_" + str(i) + ".jpg"
            # print(plotfilename)
            plt.savefig(plotfilename)
            plt.close("all")
    print("Multitasking Process finished: ", process_number)

if __name__ == "__main__":
    csv_data = []
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

    # For this to work the length of the raw sample data must be split chunks equal to the number of processes,
    h = 0
    pool_data = []
    slice_length = int(round((len(csv_data) / number_cores), 0))
    for i in range(0, len(csv_data), slice_length):
        if i == 0:
            pass
        else:
            # we set up an array to pass in to the multiprocessor pool, [data, label] matches
            # method parameters
            sliced_data = csv_data[h:i]
            print(h, i)
            dd = [sliced_data, h]
            pool_data.append(dd)
            h = i

    print("Pool data length: ", len(pool_data))

    # Multi-processing code here
    with multiprocessing.Pool(processes=number_cores) as pool:
        results = pool.starmap(process_fft_visualisation, pool_data)
        print(results)

    t_end = time.time()
    t_elapsed = (t_end - t_start) / 60
    reportstring = "Elapsed time: " + str(t_elapsed) + " minutes."
