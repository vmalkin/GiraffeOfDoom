from matplotlib import pyplot as plt
from matplotlib import ticker as ticker
import datetime

log = "logfiles//2020-10-04.csv"

def open_logfile(logfile):
    """Opens logfile, returns an array"""
    t = []
    with open(logfile, 'r') as l:
        for line in l:
            line = line.split(",")
            timestamp = line[0]
            sigma = line[2].rstrip("\n")
            dp = [timestamp, sigma]
            t.append(dp)
    return t


def create_plot(data):
    resultlist = data
    savefile = "test.jpg"
    x = []
    y = []

    for line in resultlist:
        x_val = line[0]
        y_val = line[1]
        x.append(x_val)
        y.append(y_val)
    try:
        s4, ax = plt.subplots(figsize=[20, 9], dpi=100)
        ax.scatter(x, y, marker="o", s=9, alpha=0.1, color=['black'])
        ax.grid(True, color="#ccb3b3")

        tic_space = 30
        ax.xaxis.set_major_locator(ticker.MultipleLocator(tic_space))

        ax.tick_params(axis='x', labelrotation=90)
        ax.set_xlabel("Time UTC")
        ax.set_ylabel("S4 Index", labelpad=5)
        s4.tight_layout()

        plt.title("S4 Ionospheric Index")
        plt.savefig(savefile)
        plt.close('all')
        print("S4 plot created")
    except Exception:
        print("Unable to save image file")
        plt.close('all')


data = open_logfile(log)
create_plot(data)



