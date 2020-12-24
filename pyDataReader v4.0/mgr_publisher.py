from datetime import datetime

def posix2utc(posixtime):
    timeformat = '%Y-%m-%d %H:%M:%S'
    utctime = datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime

def wrapper(current_data, publishfolder):
    savefile = publishfolder + "//dna_ambrf.csv"
    with open(savefile, "w") as s:
        s.write("UTC Datetime, Ambient Voltage" + "\n")
        for item in current_data:
            dt = posix2utc(item[0])
            data = item[1]
            dp = str(dt) + "," + str(data) + "\n"
            s.write(dp)
        s.close()