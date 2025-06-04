from scipy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt
import numpy as np
# from decimal import Decimal, getcontext, ROUND_DOWN
# getcontext().prec = 4

def make_decimal(string_value):
    result = 0
    try:
        result = float(string_value)
        result = round(result, 4)
    except ValueError:
        print("ERROR - string is not a number.")
    return result

csv_data = []

with open("dr01_24hr.csv", "r") as c:
    for line in c:
        l = line.strip()
        l = l.split(",")
        string_data = l[1]
        decimal_data = make_decimal(string_data) + 100
        csv_data.append(decimal_data)


# hertz
sample_rate = 0.5
# duration in seconds
duration = len(csv_data) * 2

# Number of samples in normalized_tone
N = int(sample_rate * duration)

norms = []
for item in csv_data:
    dd = (item / max(csv_data))
    # print(item, max(csv_data))
    normalized_tone = np.int16(dd * 32767)
    norms.append(normalized_tone)

yf = rfft(norms)
print(N)
xf = rfftfreq(N, 1 / sample_rate)

fig, ax = plt.subplots(layout="constrained", figsize=(4, 4), dpi=200)
plt.plot(xf, np.abs(yf))
ax.set_ylim([0, 5000000])
ax.set_xlim([-0, 0.005])
plt.show()
