import numpy as np
from scipy.stats import kurtosis, skew
from scipy.signal import welch, butter, sosfiltfilt, detrend
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

    # def third_central_moment(self, dataset):
    #     m3 = np.mean((dataset - np.mean(dataset)) ** 3)
    #     return m3

    def get_stddev(self, dataset):
        sd = np.std(dataset)
        return sd

    def get_mean(self, dataset):
        mn = np.mean(dataset)
        return mn

    def get_median(self, dataset):
        md = np.median(dataset)
        return md

    def get_rms(self, dataset):
        rms = np.sqrt(np.mean(np.square(dataset)))
        return rms

    # def get_skew_parsons(self, dataset):
    #     # Pearson's second coefficient of skewness
    #     mn = np.mean(dataset)
    #     md = np.median(dataset)
    #     sd = np.std(dataset)
    #     if sd != 0:
    #         skewness = (mn - md) / sd
    #     else:
    #         skewness = 0
    #     return skewness

    # def get_skew_3rdCM(self, dataset):
    #     # Skew using 3rd central moment
    #     skewness = skew(dataset, bias=False)
    #     return skewness

    def get_kurtosis(self, dataset):
        # 0: Equivalent kurtosis to a Gaussian distribution
        # Positive: Heavier tails than a Gaussian distribution
        # Negative: Lighter tails than a Gaussian distribution
        kt = kurtosis(dataset, fisher=True, bias=False)
        return kt

    # def get_spectral_entropy(self, dataset):
    #     # 2. Compute PSD with high frequency resolution
    #     nperseg = 512*1
    #     frequencies, psd = welch(dataset, fs=k.datapersecond, nperseg=nperseg)
    #
    #     # 3. Create probability distribution
    #     psd_norm = psd / np.sum(psd)
    #
    #     # 4. Filter zeros and compute Shannon Entropy
    #     psd_norm = psd_norm[psd_norm > 0]
    #     shannon_entropy = -np.sum(psd_norm * np.log2(psd_norm))
    #
    #     # 5. Normalize
    #     max_entropy = np.log2(len(psd_norm))
    #     return shannon_entropy / max_entropy


# a wee helper function to use the above class to decimate data and return it
def basic_aggregated_list(data, halfwindow, step):
    print(f'... split out data.')
    data = np.array(data)
    posix_data = data[:, 0]
    seis_data = data[:, 1]
    temp_data = data[:, 2]
    pressure_data = data[:, 3]
    # detrend the seismic data
    seis_data = detrend(seis_data, type='linear')
    aggregated_array = []
    print(f'... create aggregated array.')
    for i in range(halfwindow, len(data) - halfwindow, step):
        if i % 50000 == 0:
            print(f'... {i} / {len(data)}')
        date_start = posix_data[i - halfwindow]
        date_end = posix_data[i + halfwindow]
        d = Aggregator(date_start, date_end)
        d.data_seismo = seis_data[i - halfwindow: i + halfwindow + 1]
        d.data_pressure = pressure_data[i - halfwindow: i + halfwindow + 1]
        d.data_temperature = temp_data[i - halfwindow: i + halfwindow + 1]
        aggregated_array.append(d)
    print(f'... Aggregation finished.')
    return aggregated_array