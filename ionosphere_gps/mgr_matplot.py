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
        else:
            alt = int(alt)
            # print("Null altitude value")
        if item[4] == '':
            azi = np.nan
        else:
            azi = int(azi)
            # print("Null azimuth value")

        altitude.append(alt)
        azimuth.append(azi)

    ax.scatter(azimuth, altitude, c="seagreen")
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
        else:
            alt = int(alt)
            # print("Null altitude value")
        if item[4] == '':
            azi = np.nan
        else:
            azi = int(azi)
            # print("Null azimuth value")

        altitude.append(alt)
        azimuth.append(azi)

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(projection='polar')
    ax.scatter(azimuth, altitude, c="seagreen")
    ax.set_rmax(0)
    ax.set_rmin(90)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_title("Pretty polar error bars")
    # plt.show()
    plt.savefig(savefile)