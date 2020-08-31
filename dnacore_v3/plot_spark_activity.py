import matplotlib.pyplot as plt
import numpy as np
# Create a array of marks in different subjects scored by different students
marks = [[1.63365,
    1.05394,
    0.642,
    0.81116,
    1.86754,
    3.10922,
    2.68027,
    0.8069,
    0.89013,
    1.60795,
    0.73464,
    0.66922,
    1.11647,
    0.79267,
    1.69789,
    2.87578,
    1.71079,
    2.22781,
    4.17875,
    2,
    3.77927,
    2.16104,
    1.72438
    ]]

fig, ax = plt.subplots()
hours = ["10","11","12","13","14","15","16","17","18","19","20","21","22","23","0","1","2","3","4","5","6","7","8","9"]

ax.set_xticks(range(len(hours)))
ax.set_xticklabels(hours)

ax.imshow(marks, cmap='Greens', interpolation="hanning")
fig.tight_layout()
plt.show()