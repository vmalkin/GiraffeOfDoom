import matplotlib.pyplot as plt

data = []
with open("Ruru_Obs_1hrdx.csv", "r") as f:
    dp = f.read()
    dp = dp.strip()
    data.append(dp + "\n")

print(data)


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
    8,
    3.77927,
    2.16104,
    1.72438
    ]]
minvalue = 0
maxvalue = 9
hours = ["10","" ,"12","","14","","16","","18","","20","","22","","0","","2","","4","","6","","8",""]

# draw the heatmap
fig, ax = plt.subplots()
ax.set_xticks(range(len(hours)))
ax.set_xticklabels(hours)
ax.set_yticks([])
ax.imshow(marks, cmap='viridis', interpolation="hanning", vmin=minvalue, vmax=maxvalue)
fig.tight_layout()
plt.show()