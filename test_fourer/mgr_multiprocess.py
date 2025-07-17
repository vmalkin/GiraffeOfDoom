import multiprocessing
import matplotlib.pyplot as plt
import os
import constants as k

def plot(plotting_array, processor_id):
    # The visualisation
    # pc2 = [1 / 5, 1 / 10]
    # pc3 = [1 / 10, 1 / 45]
    # pc4 = [1 / 45, 1 / 150]
    for i in range(0, len(plotting_array)):
        if i % 100 == 0:
            print(f"Processor {processor_id}: {i} / {len(plotting_array)} plots.")
        fig, ax = plt.subplots(layout="constrained", figsize=(4, 2), dpi=200)
        plot_title = title = "FFT - " + plotting_array[i][0]
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
        # add leading zeros otherwise the images will not be sorted correctly by the moviemaker
        file_sequence = str(i).rjust(6, '0')
        plotfilename = k.img_dir + os.sep + str(processor_id) + "_" + file_sequence + ".png"
        plt.savefig(plotfilename)
        plt.close("all")


def make_plot(data):
    print("Multi-processing BEGIN")
    # Data in data array has format: [time_data, yf, xf]
    number_cores = k.number_of_cpu_cores

    pool_data = []
    # Create data pool.
    # Stolen from chatgpt - better than my janky solution!
    chunk_size = len(data) // number_cores
    pool_data = []
    sample_period = int(k.data_sample_rate * k.data_boxcar_window_in_seconds)

    # idx will get added to the pool data so the plotting function can create correctl named plots
    for idx in range(number_cores):
        start_idx = max(0, idx * chunk_size - sample_period)
        end_idx = (idx + 1) * chunk_size
        chunk = data[start_idx:end_idx]
        if len(chunk) > sample_period:
            dp = [chunk, idx]
            pool_data.append(dp)

    print(f"Pool data length: {len(pool_data)}")

    # Multi-processing code here
    with multiprocessing.Pool(processes=number_cores) as pool:
        results = pool.starmap(plot, pool_data)
        print(results)
    pool.close()
    #
    print("Multi-processing END")


