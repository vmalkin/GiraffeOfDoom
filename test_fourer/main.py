import numpy as np
from scipy.fft import rfft, rfftfreq
import requests
import matplotlib.pyplot as plt
import os
import time
import mgr_mp4
import mgr_multiprocess
import constants as k


def try_create_directory(directory):
    if os.path.isdir(directory) is False:
        print("Creating image file directory...")
        try:
            os.makedirs(directory)
            print("Directory created.")
        except:
            if not os.path.isdir(directory):
                print("Unable to create directory")


def get_url_data(pageurl):
    url = pageurl
    response = requests.get(url)
    html_lines = response.iter_lines()
    return html_lines


def process_csv_from_web(csvdata):
    return csvdata


def make_decimal(string_value):
    result = 0
    try:
        result = float(string_value)
        result = round(result, 4)
    except ValueError:
        print("ERROR - string is not a number.")
    return result


def plot(plotting_array):
    # The visualisation
    # pc2 = [1 / 5, 1 / 10]
    # pc3 = [1 / 10, 1 / 45]
    # pc4 = [1 / 45, 1 / 150]

    for i in range(0, len(plotting_array)):
        if i % 100 == 0:
            print(f"Plotting {i} / {len(plotting_array)} plots.")
        fig, ax = plt.subplots(layout="constrained", figsize=(4, 2), dpi=200)
        plot_title = plotting_array[i][0]
        yf = plotting_array[i][1]
        xf = plotting_array[i][2]
        # print(f"Min: {min(yf)}. Max: {max(yf)}")
        plt.plot(xf, yf, linewidth=1)
        ax.set_ylim([10 ** -2, 10 ** 3])
        # ax.set_xlim([0, 0.3])
        plt.yscale("log")
        plt.xscale("log")
        plt.grid()
        ax.set_title(plot_title)
        plotfilename = img_dir + os.sep + str(i) + ".png"
        plt.savefig(plotfilename)
        plt.close("all")


if __name__ == "__main__":
    t_start = time.time()
    img_dir = k.img_dir
    movie_dir = k.movie_dir
    try_create_directory(img_dir)
    try_create_directory(movie_dir)



    csv_from_web = get_url_data("http://dunedinaurora.nz/dnacore04/Ruru_Obs.csv")
    # csv_from_web = get_url_data("http://www.ruruobservatory.org.nz/dr01_24hr.csv")
    csv_from_web = process_csv_from_web(csv_from_web)

    cleaned_csv = []
    for line in csv_from_web:
        l = line.decode('utf-8')
        # l = line.strip()
        l = l.split(",")
        data_info = l[1]
        time_info = l[0]
        decimal_data = make_decimal(data_info)
        dp = [time_info, decimal_data]
        cleaned_csv.append(dp)

    # # We need positive values for this. This will shift the data up the y axis
    # # so the largest negative value is a zero, everything else should be positive
    # shift_value = math.sqrt(min(csv_data)**2)
    # csv_data_shifted = []
    # for value in csv_data:
    #     d = value + shift_value
    #     csv_data_shifted.append(d)


    # entries per second in hertz
    sample_rate = k.data_sample_rate
    duration_seconds = len(cleaned_csv) * 1 / sample_rate

    # We will sample a running window of data to process and graph
    sample_period_duration_in_seconds = k.data_boxcar_window_in_seconds
    sample_period = int(sample_rate * sample_period_duration_in_seconds)
    print(f"Beginning FFT.")
    print(f"Sampling frequency: {sample_rate} Hz, {1 / sample_rate} second period.")
    print(f"Running window length: {sample_period_duration_in_seconds} seconds.")
    print(f"Sample duration: {duration_seconds} seconds.")

    # Create a sub-array of data from the main data. This is what will be processed
    # and creates a "rolling fft". Thus, we will see changing frequencies over time.
    sample_data = cleaned_csv[:sample_period]

    plotting_array = []
    for i in range(sample_period, len(cleaned_csv)):
        sample_data.append(cleaned_csv[i])
        sample_data.pop(0)

        # Use numpy to extract the 2nd column as a new array of data.
        temp = np.array(sample_data)
        data = temp[:, 1]
        timestamp = sample_data[len(sample_data) - 1][0]

        # the Fast Fourier Transform
        yf = rfft(data)
        yf = np.abs(yf)
        xf = rfftfreq(len(data), 1 / sample_rate)

        # Create a datapoint to be appended to the array for plotting
        dp = [timestamp, yf, xf]
        plotting_array.append(dp)

    # Plot the data
    mgr_multiprocess.make_plot(plotting_array)
    # plot(plotting_array)

    # create movie
    mgr_mp4.wrapper()

    t_end = time.time()
    t_elapsed = (t_end - t_start) / 60
    print(f"Elapsed time: {t_elapsed} minutes.")
