import numpy as np
from scipy.fft import rfft, rfftfreq
import requests
import matplotlib.pyplot as plt
from matplotlib import colormaps
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


if __name__ == "__main__":
    t_start = time.time()
    img_dir = k.img_dir
    movie_dir = k.movie_dir
    try_create_directory(img_dir)
    try_create_directory(movie_dir)

    # csv_from_web = get_url_data("http://dunedinaurora.nz/dnacore04/Ruru_Obs.csv")
    csv_from_web = get_url_data("http://www.ruruobservatory.org.nz/dr01_24hr.csv")
    # csv_from_web = process_csv_from_web(csv_from_web)

    datetimes = []
    data = []
    for line in csv_from_web:
        l = line.decode('utf-8')
        # l = line.strip()
        l = l.split(",")
        data_info = l[1]
        time_info = l[0]
        decimal_data = make_decimal(data_info)
        dp = [time_info, decimal_data]
        datetimes.append(time_info)
        data.append(decimal_data)

    seconds_per_reading = 2
    sample_freq = 1 / seconds_per_reading
    sample_length = len(data)
    times = np.linspace(0, seconds_per_reading, num=sample_length)

    # diffsdata = []
    # for i in range(1, len(data)):
    #     j = data[i] - data[i - 1]
    #     diffsdata.append(j)
    #
    # plt.figure(figsize=(15, 5))
    # plt.plot(diffsdata)
    # plt.title('raw differences')
    # plt.ylabel('Signal Value')
    # plt.xlabel('Time (s)')
    # plt.ylim(-0.120, 0.120)
    # plt.show()

    plt.figure(figsize=(15, 5))
    plt.specgram(data, detrend="mean", Fs=sample_freq, vmin=-50, vmax=0, cmap='magma')
    plt.title('magnetometer spectrum')
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (s)')
    plt.colorbar()
    plt.show()