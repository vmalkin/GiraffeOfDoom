import numpy as np
from scipy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt
import constants as k

data = k.sunspot
tempdata = []
for item in data:
    d = item[1]
    tempdata.append(d)


# the Fast Fourier Transform
yf = rfft(tempdata)
yf = np.abs(yf)
xf = rfftfreq(len(tempdata), 1 / len(tempdata))

fig, ax = plt.subplots(layout="constrained", figsize=(4, 2), dpi=200)
# print(f"Min: {min(yf)}. Max: {max(yf)}")
plt.plot(xf, yf, linewidth=1)
# # ax.set_ylim([10 ** -2, 10 ** 3])
ax.set_xlim([0, 20])
# plt.yscale("log")
# plt.xscale("log")
plt.grid()
plt.show()

