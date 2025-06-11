from scipy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt
import numpy as np
import os
import time
import multiprocessing

number_cores = 12
sample_period = 1800
sample_rate = 0.5
img_dir = "images"
movie_dir = "movies"

t_start = time.time()

def try_create_directory(directory):
    if not os.path.isdir(directory):
        try:
            os.makedirs(directory)
            print(f"Directory created: {directory}")
        except Exception as e:
            print(f"Unable to create directory {directory}: {e}")

def make_decimal(string_value):
    try:
        return round(float(string_value), 4)
    except ValueError:
        print(f"ERROR - string is not a number: {string_value}")
        return 0.0

def process_fft_visualisation(data_to_process, process_number):
    print(f"Process {process_number} started")
    sample_data = data_to_process[:sample_period]  # Initialize sub-sample

    for i in range(sample_period, len(data_to_process)):
        sample_data.pop(0)
        sample_data.append(data_to_process[i])

        # FFT computation
        data_array = np.array(sample_data, dtype=np.float32)
        max_val = np.max(np.abs(data_array))
        if max_val == 0:
            continue
        normalized_data = data_array / max_val * 32767
        N = len(normalized_data)
        yf = rfft(normalized_data)
        xf = rfftfreq(N, 1 / sample_rate)

        # Visualization
        fig, ax = plt.subplots(figsize=(8, 4), dpi=200)
        ax.plot(xf, np.abs(yf))
        ax.set_ylim([100, 1e7])
        ax.set_xlim([0, 0.05])
        ax.set_yscale("log")
        plotfilename = os.path.join(img_dir, f"{process_number}_{i}.png")
        fig.savefig(plotfilename)
        plt.close(fig)

        # Print progress sparingly
        if i % 100 == 0:
            print(f"Process {process_number}: {i}/{len(data_to_process)} samples processed.")

    print(f"Process {process_number} finished")

if __name__ == "__main__":
    try_create_directory(img_dir)
    try_create_directory(movie_dir)

    csv_data = []
    with open("dr01_24hr.csv", "r") as f:
        next(f)  # skip header if needed
        for line in f:
            parts = line.strip().split(",")
            if len(parts) > 1:
                decimal_data = make_decimal(parts[1]) + 100
                csv_data.append(decimal_data)

    # Split data evenly across processes
    chunk_size = len(csv_data) // number_cores
    pool_data = []
    for idx in range(number_cores):
        start_idx = max(0, idx * chunk_size - sample_period)
        end_idx = (idx + 1) * chunk_size
        chunk = csv_data[start_idx:end_idx]
        if len(chunk) > sample_period:
            pool_data.append((chunk, idx))

    print(f"Prepared {len(pool_data)} chunks for processing.")

    with multiprocessing.Pool(processes=number_cores) as pool:
        pool.starmap(process_fft_visualisation, pool_data)

    t_end = time.time()
    print(f"Elapsed time: {(t_end - t_start)/60:.2f} minutes.")

