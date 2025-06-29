import numpy as np
from scipy.fft import rfft, rfftfreq
import requests
import matplotlib.pyplot as plt
import os
import time
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


def plot(plottingarray, processor_id):
    # The visualisation
    # pc2 = [1 / 5, 1 / 10]
    # pc3 = [1 / 10, 1 / 45]
    # pc4 = [1 / 45, 1 / 150]
    processor_id = processor_id
    for i in range(0, len(plottingarray)):
        if i % 100 == 0:
            print(f"Processor {processor_id}: {i} / {len(plottingarray)} plots.")
        fig, ax = plt.subplots(layout="constrained", figsize=(4, 2), dpi=200)
        plot_title = plotting_array[i][0]
        yf = plotting_array[i][1]
        xf = plottingarray[i][2]
        # print(f"Min: {min(yf)}. Max: {max(yf)}")
        plt.plot(xf, yf, linewidth=1)
        ax.set_ylim([10 ** -2, 10 ** 3])
        ax.set_xlim([0, 0.3])
        plt.yscale("log")
        # plt.xscale("log")
        ax.set_title(plot_title)
        plotfilename = img_dir + os.sep + str(processor_id) + "_" + str(i) + ".png"
        plt.savefig(plotfilename)
        plt.close("all")


def setup_multiprocessor_pool(csvdata, number_cores):
    # Stolen from chatgpt - better than my janky solution!
    print(csvdata[:3])
    chunk_size = len(csvdata) // number_cores
    pool_data = []
    for idx in range(number_cores):
        start_idx = max(0, idx * chunk_size - sample_period)
        end_idx = (idx + 1) * chunk_size
        chunk = csv_data[start_idx:end_idx]
        if len(chunk) > sample_period:
            pool_data.append((chunk, idx))
    return pool_data


def multiprocessor_wrapper(plotdata, processor_id):
    plot(plotdata, processor_id)


if __name__ == "__main__":
    t_start = time.time()
    img_dir = "images"
    movie_dir = "movies"
    try_create_directory(img_dir)
    try_create_directory(movie_dir)

    csv_data = []
    time_data = []
    csv_from_web = get_url_data("http://www.ruruobservatory.org.nz/dr01_24hr.csv")
    csv_from_web = process_csv_from_web(csv_from_web)

    for line in csv_from_web:
        l = line.decode('utf-8')
        # l = line.strip()
        l = l.split(",")
        data_info = l[1]
        time_info = l[0]
        decimal_data = make_decimal(data_info)
        csv_data.append(decimal_data)
        time_data.append(time_info)

    # # We need positive values for this. This will shift the data up the y axis
    # # so the largest negative value is a zero, everything else should be positive
    # shift_value = math.sqrt(min(csv_data)**2)
    # csv_data_shifted = []
    # for value in csv_data:
    #     d = value + shift_value
    #     csv_data_shifted.append(d)
    csv_data_shifted = csv_data

    # entries per second in hertz
    plotting_array = []
    sample_rate = 0.5
    duration_seconds = len(csv_data_shifted) * 1 / sample_rate
    # # Time vector
    # t = np.linspace(0, duration_seconds, sample_rate, endpoint=False)

    # We will sample a running window of data to process and graph
    sample_period_duration_in_seconds = 60 * 20
    sample_period = int(sample_rate * sample_period_duration_in_seconds)
    print(f"Beginning FFT.")
    print(f"Sampling frequency: {sample_rate} Hz, {1 / sample_rate} second period.")
    print(f"Running window length: {sample_period_duration_in_seconds} seconds.")
    print(f"Sample duration: {duration_seconds} seconds.")
    sample_data = csv_data_shifted[:sample_period]
    sample_time = time_data[:sample_period]
    for i in range(sample_period, len(csv_data_shifted)):
        sample_data.pop(0)
        sample_data.append(csv_data_shifted[i])
        # the Fast Fourier Transform
        yf = rfft(sample_data)
        yf = np.abs(yf)
        # print(len(yf))
        xf = rfftfreq(len(sample_data), 1 / sample_rate)
        dp = [time_data[i], yf, xf]
        plotting_array.append(dp)

    number_of_cores = 10
    pooldata = setup_multiprocessor_pool(plotting_array, number_of_cores)
    # # Multi-processing code here
    # with multiprocessing.Pool(processes=number_of_cores) as pool:
    #     results = pool.starmap(multiprocessor_wrapper, pooldata)
    #     print(results)
    # pool.close()

    # print("Plotting..")
    # plot(plotting_array)

    t_end = time.time()
    t_elapsed = (t_end - t_start) / 60
    print(f"Elapsed time: {t_elapsed} minutes.")
