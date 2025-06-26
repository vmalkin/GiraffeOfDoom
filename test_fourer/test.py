import math
import numpy as np
from scipy.fft import rfft, rfftfreq
import requests
import matplotlib.pyplot as plt
import os
import multiprocessing


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
    img_dir = "images"
    movie_dir = "movies"
    try_create_directory(img_dir)
    try_create_directory(movie_dir)

    csv_data = []
    csv_from_web = get_url_data("http://www.ruruobservatory.org.nz/dr01_24hr.csv")
    csv_from_web = process_csv_from_web(csv_from_web)

    for line in csv_from_web:
        l = line.decode('utf-8')
        # l = line.strip()
        l = l.split(",")
        string_data = l[1]
        decimal_data = make_decimal(string_data)
        csv_data.append(decimal_data)

    # We need positive values for this
    shift_value = math.sqrt(min(csv_data)**2)
    csv_data_shifted = []
    for value in csv_data:
        d = value + shift_value + 100
        csv_data_shifted.append(d)

    # entries per second in hertz
    sample_rate = 0.5
    duration_seconds = len(csv_data_shifted) * sample_rate
    # # Time vector
    # t = np.linspace(0, duration_seconds, sample_rate, endpoint=False)

    # We will sample a running window of data to process and graph
    sample_period_duration_in_seconds = 60 * 60
    sample_period = int(sample_rate * sample_period_duration_in_seconds)
    sample_data = csv_data_shifted[:sample_period]
    for i in range(sample_period, len(csv_data_shifted)):
        sample_data.pop(0)
        sample_data.append(csv_data_shifted[i])
        if i % 100 == 0:
            print(f"Processed: {i} / {len(csv_data_shifted)}")

        # the Fast Fourier Transform
        yf = rfft(sample_data)
        # print(len(yf))
        xf = rfftfreq(len(sample_data), 1 / sample_rate)

        # Plotting
        fig, ax = plt.subplots(layout="constrained", figsize=(8, 4), dpi=200)
        plt.plot(xf, np.abs(yf))
        plt.title('FFT of data')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
        plt.yscale("log")
        plt.grid()
        ax.set_ylim([0.01, 10000000])
        ax.set_xlim([0, 0.25])
        process_number = 0
        plotfilename = img_dir + os.sep + str(process_number) + "_" + str(i) + ".png"
        plt.savefig(plotfilename)
        plt.close("all")
        # plt.show()


        # # For this to work the length of the raw sample data must be split chunks equal to the number of processes,
        # # h = 0
        # pool_data = []
        # # Stolen from chatgpt - better than my janky solution!
        # chunk_size = len(csv_data) // number_cores
        # pool_data = []
        # for idx in range(number_cores):
        #     start_idx = max(0, idx * chunk_size - sample_period)
        #     end_idx = (idx + 1) * chunk_size
        #     chunk = csv_data[start_idx:end_idx]
        #     if len(chunk) > sample_period:
        #         pool_data.append((chunk, idx))
        #
        # print(f"Pool data length: {len(pool_data)}")
        #
        # # Multi-processing code here
        # with multiprocessing.Pool(processes=number_cores) as pool:
        #     results = pool.starmap(process_fft_visualisation, pool_data)
        #     print(results)
        # pool.close()