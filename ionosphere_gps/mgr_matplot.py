import matplotlib.pyplot as plt
import numpy as np

plt.style.use('_mpl-gallery')

def plot_alt_az(queryresult, savefile):
    fig, ax = plt.subplots(layout="constrained", figsize=(9,3), dpi=140)
    # datetime = []
    altitude = []
    azimuth = []
    for item in queryresult:
        # datetime.append(item[2])
        alt = item[3]
        azi = item[4]

        if item[3] == '':
            alt = np.nan
            # print("Null altitude value")
        if item[4] == '':
            azi = np.nan
            # print("Null azimuth value")

        altitude.append(alt)
        azimuth.append(azi)

    ax.scatter(azimuth, altitude)
    ax.set(xlim=(0, 360), ylim=(0, 90))
    plt.savefig(savefile)
    # plt.show()

def plot_polar_positions(queryresult, savefile):
    altitude = []
    azimuth = []
    for item in queryresult:
        # datetime.append(item[2])
        alt = item[3]
        azi = item[4]

        if item[3] == '':
            alt = np.nan
            # print("Null altitude value")
        if item[4] == '':
            azi = np.nan
            # print("Null azimuth value")

        altitude.append(alt)
        azimuth.append(azi)

    fig = plt.figure()
    ax = fig.add_subplot(projection='polar', layout="constrained", figsize=(5,5), dpi=140)
    ax.scatter(azimuth, altitude, cmap='hsv', alpha=0.75)
    plt.show