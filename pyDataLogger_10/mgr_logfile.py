from standard_stuff import posix2utc

def wrapper(data, savefilepath):
    # Current data is CSV file with format "posixtime, datavalue"
    currentdata = data
    # tmp = []
    savefile_name = savefilepath

    with open(savefile_name, "w") as s:
        s.write("Datetime UTC, Datavalue Arbitrary Units\n")
        for item in currentdata:
            dt = posix2utc(item[0], '%Y-%m-%d %H:%M:%S')
            da = str(item[1])
            dp = dt + "," + da + "\n"
            s.write(dp)
    s.close()
    print("*** Daily Logfile: Saved " + savefile_name)
