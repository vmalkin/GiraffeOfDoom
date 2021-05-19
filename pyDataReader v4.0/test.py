import mgr_detrended

data = []
with open("arraysave.csv", "r") as d:
    for line in d:
        line.strip()
        i = line.split(",")
        dt = int(float(i[0]))
        da = i[1]
        l = str(dt) + "," + da
        data.append(l)

mgr_detrended.wrapper(data, "publish")