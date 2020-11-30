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
    pass


data = open_logfile(log)
create_plot(data)



