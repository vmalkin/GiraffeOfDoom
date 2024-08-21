import emd

sample_rate = 1000
seconds = 10
num_samples = sample_rate*seconds

import numpy as np
time_vect = np.linspace(0, seconds, num_samples)

freq = 5
nonlinearity_deg = .25  # change extent of deformation from sinusoidal shape [-1 to 1]
nonlinearity_phi = -np.pi/4  # change left-right skew of deformation [-pi to pi]
x = emd.simulate.abreu2010(freq, nonlinearity_deg, nonlinearity_phi, sample_rate, seconds)
# x += np.cos(2*np.pi*1*time_vect)
print(x.shape)

imf = emd.sift.sift(x)
print(imf)
IP, IF, IA = emd.spectra.frequency_transform(imf, sample_rate, 'hilbert')
freq_range = (0, 10, 100)  # 0 to 10Hz in 100 steps
f, hht = emd.spectra.hilberthuang(IF, IA, freq_range, sum_time=False)

# import matplotlib.pyplot as plt
# plt.figure(figsize=(16, 8))
# plt.subplot(211, frameon=False)
# plt.plot(time_vect, x, 'k')
# plt.plot(time_vect, imf[:, 0]-4, 'r')
# plt.plot(time_vect, imf[:, 1]-8, 'g')
# plt.plot(time_vect, imf[:, 2]-12, 'b')
# # plt.xlim(time_vect[0], time_vect[-1])
# plt.grid(True)
# plt.subplot(212)
# # plt.pcolormesh(time_vect, f, hht, cmap='ocean_r')
# plt.ylabel('Frequency (Hz)')
# plt.xlabel('Time (secs)')
# plt.grid(True)
# plt.show()