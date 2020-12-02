from matplotlib import pyplot as plt

class GPSSatellite:
    def __init__(self, sat_name):
        self.name = sat_name
        self.posixtime = []
        self.alt = []
        self.az = []
        self.snr = []
        self.s4 = []


def create_satellite_list(constellationname):
    returnlist = []
    for i in range(0, 300):
        name = constellationname + str(i)
        gps = GPSSatellite(name)
        returnlist.append(gps)
    return returnlist


def create_chart(sat):
    name = sat.name + ".jpg"
    x = sat.posixtime
    y1 = sat.alt
    y2 = sat.snr
    y3 = sat.s4
    s4, ax = plt.subplots(figsize=[3,2], dpi=100)
    plt.plot(x, y1, color = "red")
    plt.plot(x, y2, color = "black")
    plt.plot(x, y3, color = "blue")
    plt.savefig(name)




def create_individual_plots(resultlist):
    GPGSV = create_satellite_list("gps_")
    GLGSV = create_satellite_list("glonass_")

    #  Resultlist should have the format
    # sat_id, posixtime, alt, az, s4, snr
    for sat in resultlist:
        detail = sat[0].split("_")
        name = detail[0]
        number = int(detail[1])
        if name == "gps":
            GPGSV[number].name = sat[0]
            GPGSV[number].posixtime.append(sat[1])
            GPGSV[number].alt.append(sat[2])
            GPGSV[number].az.append(sat[3])
            GPGSV[number].s4.append(sat[4])
            GPGSV[number].snr.append(sat[5])
        if name == "glonass":
            GLGSV[number].name = sat[0]
            GLGSV[number].posixtime.append(sat[1])
            GLGSV[number].alt.append(sat[2])
            GLGSV[number].az.append(sat[3])
            GLGSV[number].s4.append(sat[4])
            GLGSV[number].snr.append(sat[5])

    for sat in GPGSV:
        if len(sat.snr) > 1:
            create_chart(sat)

    for sat in GLGSV:
        if len(sat.snr) > 1:
            create_chart(sat)