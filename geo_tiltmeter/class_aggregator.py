import numpy as np
from scipy.stats import kurtosis, skew
from scipy.signal import welch, butter, sosfiltfilt
import constants as k
from datetime import datetime, timezone


class Aggregator:
    def __init__(self, posixstart, posixstop):
        # self.data_null = np.nan
        self.data_null = 0
        self.date_start = posixstart  # should be POSIX values
        self.date_stop = posixstop  # should be POSIX values
        self.data_seismo = []
        self.data_temperature = []
        self.data_pressure = []

    def get_data_avg(self, dataset):
        # return the median value of the data set. If the set is empty, return a null
        val_avg = self.data_null
        if len(dataset) >= 1:
            val_avg = round(np.mean(dataset), 4)
        if np.isnan(val_avg):
            val_avg = self.data_null
        return val_avg

    def get_avg_posix(self):
        avg_time = round((self.date_start + self.date_stop) / 2, 4)
        return avg_time

    def return_utc_timeobject(self, psx):
        tim = datetime.fromtimestamp(psx, tz=timezone.utc)
        return tim

    # def get_rms(self, dataset):
    #     rms = np.sqrt(np.mean(np.square(dataset))) - np.mean(dataset)
    #     return rms
    def third_central_moment(self, dataset):
        m3 = np.mean((dataset - np.mean(dataset)) ** 3)
        return m3

    def get_stddev(self, dataset):
        sd = np.std(dataset)
        return sd

    def get_mean(self, dataset):
        mn = np.mean(dataset)
        return mn

    def get_median(self, dataset):
        md = np.median(dataset)
        return md

    def get_skewness(self, dataset):
        # Pearson's second coefficient of skewness
        mn = np.mean(dataset)
        md = np.median(dataset)
        sd = np.std(dataset)
        if sd != 0:
            skewness = (mn - md) / sd
        else:
            skewness = 0
        return skewness

    # def get_skewness(self, dataset):
    #     # Skew using 3rd central moment
    #     skewness = skew(dataset, bias=False)
    #     return skewness

    def get_kurtosis(self, dataset):
        # 0: Equivalent kurtosis to a Gaussian distribution
        # Positive: Heavier tails than a Gaussian distribution
        # Negative: Lighter tails than a Gaussian distribution
        kt = kurtosis(dataset, fisher=True, bias=False)
        return kt

    def get_spectral_entropy(self, dataset):
        # The spectral entropy captures the "peakiness" of a spectrum, where a flat distribution
        # has high entropy and sharp peaks have low entropy
        # Higher entropy indicates more unpredictability and information content,
        # while lower entropy suggests predictability and less new information
        # # 1. Pre-filter the raw data to isolate 0.03 Hz to 0.3 Hz (3s to 33s periods)
        # # This strips out 0Hz DC drift and high-frequency cultural noise
        # # use a 4-pole butterworth filter to get the seismic signals
        # sos = butter(
        #     4,
        #     [0.0001, 0.3],
        #     btype='bandpass',
        #     fs=k.datapersecond,
        #     output='sos'
        # )
        # filtered = sosfiltfilt(sos, data)

        # 2. Compute PSD with high frequency resolution
        nperseg = 4096
        frequencies, psd = welch(dataset, fs=k.datapersecond, nperseg=nperseg)

        # 3. Create probability distribution
        psd_norm = psd / np.sum(psd)

        # 4. Filter zeros and compute Shannon Entropy
        psd_norm = psd_norm[psd_norm > 0]
        shannon_entropy = -np.sum(psd_norm * np.log2(psd_norm))

        # 5. Normalize
        max_entropy = np.log2(len(psd_norm))
        return shannon_entropy / max_entropy

# This function performs aggregation using the Aggregator class
# querydata has the format [utc_object_time, seismic_data, temperature_data, pressure_data]
def aggregate_data(halfwindow, step, querydata, mode):
    # windowsize needs to be at least 1
    # PASS 1 - Set up the array
    # print("PASS 1 - Setting up aggregating array")
    tiltdata = np.array(querydata)
    utc_object_time = tiltdata[:,0]
    seismic_data = tiltdata[:,1]
    temperature_data = tiltdata[:,2]
    pressure_data = tiltdata[:,3]
    aggregate_array = []
    for i in range(halfwindow, len(querydata) - halfwindow, step):
        date_start = utc_object_time[i - halfwindow]
        date_end = utc_object_time[i + halfwindow]
        d = Aggregator(date_start, date_end)
        d.data_seismo = seismic_data[i - halfwindow: i + halfwindow + 1]
        d.data_pressure = pressure_data[i - halfwindow: i + halfwindow + 1]
        d.data_temperature = temperature_data[i - halfwindow: i + halfwindow + 1]
        aggregate_array.append(d)

    # PASS 2 - Use aggregator class functions to create plotting data
    # print("PASS 2 - Create and return plotting array.")
    utc_object_time = []
    seismic_data = []
    temperature_data = []
    pressure_data = []
    rms_data = []
    stddev_data = []
    mean_data = []
    median_data = []
    skews_data = []
    kurts_data = []
    spectral_entropy_data = []
    #
    if mode == 'basic':
        print(f'{mode} mode')
    for i in range(1, len(aggregate_array)):
        # if i % 10000 == 0:
        #     print(f'Basic data {round(i / len(aggregate_array), 2)} completed.')
        tim = aggregate_array[i].get_avg_posix()
        tim = aggregate_array[i].return_utc_timeobject(tim)
        #
        siz = aggregate_array[i].get_data_avg(aggregate_array[i].data_seismo)
        tmp = aggregate_array[i].get_data_avg(aggregate_array[i].data_temperature)
        prs = aggregate_array[i].get_data_avg(aggregate_array[i].data_pressure)
        utc_object_time.append(tim)
        seismic_data.append(siz)
        temperature_data.append(tmp)
        pressure_data.append(prs)

    if mode == 'stats':
        print(f'{mode} mode')
        for i in range(1, len(aggregate_array)):
            if i % 10000 == 0:
                print(f'Full data {round(i/len(aggregate_array), 2)} completed.')
            # rms = aggregate_array[i].get_rms(aggregate_array[i].data_seismo)
            sdv = aggregate_array[i].get_stddev(aggregate_array[i].data_seismo)
            men = aggregate_array[i].get_mean(aggregate_array[i].data_seismo)
            med = aggregate_array[i].get_median(aggregate_array[i].data_seismo)
            skw = aggregate_array[i].get_skewness(aggregate_array[i].data_seismo)
            krt = aggregate_array[i].get_kurtosis(aggregate_array[i].data_seismo)
            ent = aggregate_array[i].get_spectral_entropy(aggregate_array[i].data_temperature)

            # rms_data.append(rms)
            stddev_data.append(sdv)
            mean_data.append(men)
            median_data.append(med)
            skews_data.append(skw)
            kurts_data.append(krt)
            spectral_entropy_data.append(ent)

    # return plotting_data
    return [
        ["UTC", "x-axis title/description.", utc_object_time],
        ["Tilt", "Unprocessed tilt data.", seismic_data],
        ["Device Temp", "Tiltmeter temperature.", temperature_data],
        ["Pressure", "Ambient pressure not corrected for height.", pressure_data],
        ["Mean", "", mean_data],
        ["Median", "", median_data],
        # ["Root Mean Square", "", rms_data],
        ["Standard Deviation", "SD of the data.", stddev_data],
        ["Skew", "Skew using 3rd central moment.", skews_data],
        ["Kurtosis", "", kurts_data],
        ["Spectral Entropy", "Spectral peakiness. High is more unpredicatable, more info. Low is less new info.", spectral_entropy_data]
    ]