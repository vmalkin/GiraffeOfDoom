import matplotlib.pyplot as plt
import numpy as np



# def plot_alt_az(queryresult, savefile):
#     fig, ax = plt.subplots(layout="constrained", figsize=(15,5), dpi=140)
#     # datetime = []
#     altitude = []
#     azimuth = []
#     signalnoise = []
#     for item in queryresult:
#         # datetime.append(item[2])
#         alt = item[3]
#         azi = item[4]
#         snr = item[5]
#
#         if item[3] == '':
#             alt = np.nan
#         else:
#             alt = int(alt)
#             # print("Null altitude value")
#         if item[4] == '':
#             azi = np.nan
#         else:
#             azi = int(azi)
#             # print("Null azimuth value")
#         if item[5] == '':
#             snr = np.nan
#         else:
#             snr = int(snr)
#
#         altitude.append(alt)
#         azimuth.append(azi)
#         signalnoise.append(snr)
#
#     ax.scatter(azimuth, altitude, s=50, c=signalnoise, cmap='afmhot', alpha=0.5)
#     ax.set(xlim=(0, 360), ylim=(0, 90))
#     ax.set_title("GPS Tracks - 25 hours")
#     plt.savefig(savefile)
#     # plt.show()
#
# def plot_polar_positions(queryresult, savefile):
#     # Polar plot Theta axis is in radians!
#     altitude = []
#     azimuth = []
#     for item in queryresult:
#         # datetime.append(item[2])
#         alt = item[3]
#         azi = item[4]
#
#         if item[3] == '':
#             alt = np.nan
#         else:
#             alt = int(alt)
#             # print("Null altitude value")
#         if item[4] == '':
#             azi = np.nan
#         else:
#             azi = azi * (np.pi / 180)
#             # print("Null azimuth value")
#
#         altitude.append(alt)
#         azimuth.append(azi)
#
#     fig = plt.figure(figsize=(6, 6), dpi=140)
#     ax = fig.add_subplot(projection='polar')
#
#     ax.scatter(azimuth, altitude, s=6, c="seagreen")
#     ax.set_rmax(0)
#     ax.set_rmin(90)
#     ax.set_theta_zero_location("N")
#     ax.set_theta_direction(-1)
#     ax.set_title("GPS Tracks - 24 hours")
#     # plt.show()
#     plt.savefig(savefile)

def plot_polar_noise(queryresult, savefile):
    # plt.style.use('_mpl-gallery')
    # Polar plot Theta axis is in radians!
    altitude = []
    azimuth = []
    signalnoise = []
    for item in queryresult:
        # datetime.append(item[2])
        alt = item[3]
        azi = item[4]
        snr = item[5]

        if item[3] == '':
            alt = np.nan
        else:
            alt = int(alt)
            # print("Null altitude value")
        if item[4] == '':
            azi = np.nan
        else:
            # azimuths have to be in radians, even tho the graph shows them as degrees
            azi = azi * (np.pi / 180)
            # print("Null azimuth value")
        if item[5] == '':
            snr = np.nan
        else:
            snr = int(snr)
            # print("Null altitude value")

        altitude.append(alt)
        azimuth.append(azi)
        signalnoise.append(snr)

    fig = plt.figure(layout="constrained", figsize=(6, 6), dpi=140)
    ax = fig.add_subplot(projection='polar')


    ax.scatter(azimuth, altitude, s=10, c=signalnoise, cmap='Blues', alpha=0.5)
    ax.set_rmax(0)
    ax.set_rmin(90)
    ax.set_theta_zero_location("S")
    ax.set_theta_direction(1)
    ax.set_title("GPS SNR Tracks - 24 hours")
    # plt.show()
    plt.savefig(savefile)