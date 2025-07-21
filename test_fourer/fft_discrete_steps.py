import matplotlib.axes
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
import standard_stuff


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


def reverse_data(data):
    data.reverse()



def split_data(spectrumdata, window_time_in_seconds):
    chunksize = int(window_time_in_seconds / seconds_per_reading)
    # print(f"Size of data chunk: {chunksize}")
    number_of_chunks = (len(spectrumdata) // chunksize) + 1
    # print(f"Number of chunks: {number_of_chunks}")
    returnarray = []

    for i in range(0, number_of_chunks):
        j = spectrumdata[i * chunksize:(i + 1) * chunksize]
        # print(f"{i * chunksize}:{(i + 1) * chunksize} {len(j)}")
        returnarray.append(j)
    # print(f"Length of return array: {len(returnarray)}")
    return returnarray

def perform_fft(item, seconds_per_data):
    sample_freq = 1 / seconds_per_data
    try:
        yf = rfft(item)
        yf = np.abs(yf)
        xf = rfftfreq(len(item), 1 / sample_freq)
        dp = [xf, yf]
        return dp
    except:
        return ("error_fft")


def plot_fft(fft_data, times, file_name):
    # fft data is [xf, yf]
    xf = fft_data[0]
    x_scale_title = "Period - Hz"
    # xxf = []
    # for item in xf:
    #     try:
    #         d = 1 / item
    #     except:
    #         d = 0
    #     xxf.append(d)
    # x_scale_title = "Period - Seconds"

    yf = fft_data[1]
    startplot = times[0]
    endplot = times[len(times) - 1]

    plt.figure(figsize=(15, 5))

    plt.plot(xf, yf, linewidth=1)
    title = "FFT - " + startplot + " to " + endplot
    plt.title(title)
    plt.xlabel = x_scale_title

    ann_pos = 5**-1
    plt.annotate("2s", xy=(ann_pos, 10**-1.8),xytext=(ann_pos, 10 ** -1.8), fontsize=8, color='red', bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos = 10 ** -1
    plt.annotate("10s", xy=(ann_pos, 10 ** -1.8), xytext=(ann_pos, 10 ** -1.8), fontsize=8, color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos = 10 **-2
    plt.annotate("100s", xy=(ann_pos, 10 ** -1.8), xytext=(ann_pos, 10 ** -1.8), fontsize=8, color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    ann_pos = 10 **-3
    plt.annotate("16m", xy=(ann_pos, 10 ** -1.8), xytext=(ann_pos, 10 ** -1.8), fontsize=8, color='red',
                 bbox=dict(boxstyle="round", fc="1", color='red'))

    plt.ylim(10**-2, 10**4)
    # ax.set_xlim([0, 0.3])
    plt.yscale("log")
    plt.xscale("log")
    plt.grid()
    savefile = discreet_step_dir + os.sep + "fft-" + file_name + ".png"
    plt.savefig(savefile)
    plt.close()


if __name__ == "__main__":
    t_start = time.time()

    discreet_step_dir = "discreet"
    try_create_directory(discreet_step_dir)

    seconds_per_reading = 2
    frequency = 1 / seconds_per_reading

    # csv_from_web = get_url_data("http://dunedinaurora.nz/dnacore04/Ruru_Obs.csv")
    csv_from_web = get_url_data("http://www.ruruobservatory.org.nz/dr01_24hr.csv")
    # csv_from_web = process_csv_from_web(csv_from_web)

    # datetimes = []
    data = []
    for line in csv_from_web:
        l = line.decode('utf-8')
        # l = line.strip()
        l = l.split(",")
        data_info = l[1]
        time_info = l[0]
        decimal_data = make_decimal(data_info)
        dp = [time_info, decimal_data]
        # datetimes.append(time_info)
        data.append(dp)
    # Remove the column headers from the datetime information
    # datetimes.pop(0)
    data.pop(0)
    split_interval_seconds = 60 * 60

    # we want the most recent data to be a complete segment, so reverse the data before splitting it
    reverse_data(data)
    data_segments = split_data(data, split_interval_seconds)
    # revert segments to correct chronological order, but data withing segments will be reversed. FIx in loop
    reverse_data(data_segments)
    for i in range(0, len(data_segments)):
        # sort segment data into correct chronological order
        reverse_data(data_segments[i])
        file_name = str(len(data_segments) - i)
        segment_times = []
        segment_data = []
        for j in range(0, len(data_segments[i])):
            utc_times = data_segments[i][j][0]
            data = data_segments[i][j][1]
            segment_times.append(utc_times)
            segment_data.append(data)

        fft_data = perform_fft(segment_data, seconds_per_reading)
        plot_fft(fft_data, segment_times, str(i))

    #     vmin = min(data)
    #     vmax = max(data)
    # # seconds_per_reading = 2
    # # sample_freq = 1 / seconds_per_reading
    #     sample_length = len(data)
    #     times = np.linspace(0, seconds_per_reading, num=sample_length)
    #
    #     # # Plot FFT spectrogram
    #     plt.figure(figsize=(15, 6))
    #     plt.specgram(data, detrend="mean", Fs=frequency, vmin=vmin, vmax=vmax, cmap='magma')
    #     title = "Spectrum last 24 hrs - " + 1
    #     plt.subplots_adjust(bottom=0.25)
    #     plt.title(title)
    #
    #     # arraylength = len(datetimes)
    #     # newtickarray = []
    #     # newdatetime = []
    #     # only have tick labels every few ticks
    #     # interval  = 60 * 60
    #     # tick_positions = np.arange(0,arraylength)
    #     # for i in range(0, arraylength):
    #     #     if i * frequency % interval == 0:
    #     #         newtickarray.append(i)
    #     #         newdatetime.append(datetimes[i])
    #
    #     # plt.xticks(newtickarray, newdatetime, rotation=45)
    #     plt.ylabel('Frequency (Hz)')
    #     plt.xlabel('Time (s)')
    #     plt.colorbar()
    #     savefile = "spec-" + i + ".png"
    #     plt.savefig(savefile)

