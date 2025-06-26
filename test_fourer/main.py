from scipy.fft import rfft, rfftfreq
import requests
import matplotlib.pyplot as plt
import numpy as np
import os
import time
import multiprocessing
import mgr_mp4



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

def process_fft_visualisation(data_to_process, sample_period, process_number):
    print("Multitasking Process started: ", process_number)
    # The number of samples to do the FFT for. Part of a subset of the full date
    sample_data = data_to_process[:sample_period]

    for i in range(sample_period, len(data_to_process)):
        sample_data.pop(0)
        # Build up the sub-sample array from the main data
        sample_data.append(data_to_process[i])
        if i % 100 == 0:
            print(f"process {process_number}: {i} / {len(data_to_process)}")

        # duration in seconds
        duration = len(sample_data) * (1 / sample_rate)

        # Number of samples in normalized_tone
        N = int(sample_rate * duration)

        # the FFT calculation
        norms = []
        for item in sample_data:
            dd = (item / max(sample_data))
            normalized_tone = np.int16(dd * 32767)
            norms.append(normalized_tone)
        yf = rfft(norms)
        xf = rfftfreq(N, 1 / sample_rate)

        # The visualisation
        fig, ax = plt.subplots(layout="constrained", figsize=(8, 4), dpi=200)
        plt.plot(xf, np.abs(yf))
        ax.set_ylim([50, 10000000])
        ax.set_xlim([0, 0.25])
        plt.yscale("log")
        plotfilename = img_dir + os.sep + str(process_number) + "_" + str(i) + ".png"
        plt.savefig(plotfilename)
        plt.close("all")
    print(f"Multitasking Process finished: {process_number}")


def get_url_data(pageurl):
    url = pageurl
    response = requests.get(url)
    html_lines = response.iter_lines()
    return html_lines


def process_csv_from_web(csvdata):
    return csvdata


if __name__ == "__main__":
    number_cores = 5
    sample_period = int(60 * 30)
    # hertz
    sample_rate = 0.5
    img_dir = "images"
    movie_dir = "movies"

    csv_data = []
    try_create_directory(img_dir)
    try_create_directory(movie_dir)
    csv_from_web = get_url_data("http://www.ruruobservatory.org.nz/dr01_24hr.csv")
    csv_from_web = process_csv_from_web(csv_from_web)

    # for line in csv_from_web:
    #     l = line.decode('utf-8')
    #     # l = line.strip()
    #     l = l.split(",")
    #     string_data = l[1]
    #
    #     # this is weird, why do we need to add 100 here?
    #     decimal_data = make_decimal(string_data) + 100
    #     # np.append(csv_data, decimal_data)
    #     csv_data.append(decimal_data)

    with open("test.csv", "r") as c:
        for line in c:
            l = line.strip()
            ll = l.split(",")
            dp = float(ll[1])
            csv_data.append(dp)

    # process_fft_visualisation(csv_data, 0)
    # For this to work the length of the raw sample data must be split chunks equal to the number of processes,
    # h = 0
    pool_data = []
    # Stolen from chatgpt - better than my janky solution!
    chunk_size = len(csv_data) // number_cores
    pool_data = []
    for idx in range(number_cores):
        start_idx = max(0, idx * chunk_size - sample_period)
        end_idx = (idx + 1) * chunk_size
        chunk = csv_data[start_idx:end_idx]
        if len(chunk) > sample_period:
            pool_data.append((chunk, idx))

    print(f"Pool data length: {len(pool_data)}")

    # Multi-processing code here
    with multiprocessing.Pool(processes=number_cores) as pool:
        results = pool.starmap(process_fft_visualisation, pool_data)
        print(results)
    pool.close()

    mgr_mp4.wrapper()

    t_end = time.time()
    t_elapsed = (t_end - t_start) / 60
    print(f"Elapsed time: {t_elapsed} minutes.")
