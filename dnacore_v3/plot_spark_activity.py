from matplotlib import pyplot as plt
import numpy as np

# THis would be from a JSON file list of data in [hour, value] format
data = [[0,4],[0,4],[0,6],[0,8]]

x = []
y = []

for line in data:
        x.append(line[0])
        y.append(line[1])

fig, ax = plt.subplots()
im = ax.imshow(data)
fig.tight_layout()

plt.show()