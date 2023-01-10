from standard_stuff import posix2utc

def wrapper(currentdata, logfile_directory):
    # Current data is CSV file with format "posixtime, datavalue"
    tmp = []
    savefile_name = logfile_directory + "//" +  posix2utc(currentdata[0][0], '%Y-%m-%d') + ".csv"

    with open(savefile_name, "w") as s:
        s.write("Datetime UTC, Datavalue Arbitrary Units\n")
        for item in currentdata:
            dt = posix2utc(item[0], '%Y-%m-%d %H:%M:%S')
            da = str(item[1])
            dp = dt + "," + da + "\n"
            s.write(dp)
    s.close()
    print("*** Daily Logfile: Created")
