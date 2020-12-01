from matplotlib import pyplot as plt
from matplotlib import ticker as ticker
import os

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


def create_plot(data, filename):
    resultlist = data
    savefile = filename
    x = []
    y = []

    for line in resultlist:
        x_val = line[0]
        y_val = line[1]
        x.append(x_val)
        y.append(y_val)
    try:
        s4, ax = plt.subplots(figsize=[10, 5])
        ax.bar(x, y, color=['red'], width = 1)
        # ax.grid(True, color="#ccb3b3")

        tic_space = 30
        ax.xaxis.set_major_locator(ticker.MultipleLocator(tic_space))

        ax.tick_params(axis='x', labelrotation=90)
        ax.set_xlabel("Time UTC")
        ax.set_ylabel("S4 Index", labelpad=5)
        # s4.tight_layout()

        plt.title("S4 Ionospheric Index")
        plt.savefig(savefile)
        plt.close('all')
        print("S4 plot created")
    except Exception:
        print("Unable to save image file")
        plt.close('all')


if __name__ == "__main__":
    filedir = "logfiles/"
    filelist = "files.txt"
    files_to_process = filedir + filelist

    try:
        os.makedirs("images")
        print("Logfile directory created.")
    except:
        if not os.path.isdir("images"):
            print("Unable to create log directory")

    with open(files_to_process, 'r') as f:
        for item in f:
            nomen = item.split(".")
            nomen = nomen[0]
            graph = "images//" + nomen + ".jpg"
            data = nomen + ".csv"
            filename = filedir + data
            t = open_logfile(filename)
            create_plot(t, graph)

    print("FINISHED")





