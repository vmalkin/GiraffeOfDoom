import DataPoint

dp1 = DataPoint.DataPoint("2016-05-26 1:01:00",1,2,3)
dp2 = DataPoint.DataPoint("2016-05-26 1:02:00",2,2,3)
dp3 = DataPoint.DataPoint("2016-05-26 1:03:00",3,2,3)
dp4 = DataPoint.DataPoint("2016-05-26 1:04:00",10,2,10) # BLIP
dp5 = DataPoint.DataPoint("2016-05-26 1:05:00",3,2,3)
dp6 = DataPoint.DataPoint("2016-05-26 1:06:00",2,2,3)
dp7 = DataPoint.DataPoint("2016-05-26 1:07:00",1,2,3)
dp8 = DataPoint.DataPoint("2016-05-26 1:08:00",2,2,3)
dp9 = DataPoint.DataPoint("2016-05-26 1:09:00",3,2,3)
dp10 = DataPoint.DataPoint("2016-05-26 1:10:00",4,2,3)

testdata = [dp1 ,dp2, dp3, dp4, dp5, dp6, dp7, dp8, dp9, dp10]


def median_filter(arraydata):
    outputarray = []

    for i in range(1,len(arraydata)-1):
        xlist = []
        ylist = []
        zlist = []

        for j in range(-1,2):    # -1, 0, 1
            k = i + j
            xlist.append(arraydata[k].raw_x)
            ylist.append(arraydata[k].raw_y)
            zlist.append(arraydata[k].raw_z)

        xlist.sort()
        ylist.sort()
        zlist.sort()

        dp = DataPoint.DataPoint(arraydata[i].dateTime, xlist[1],ylist[1], zlist[1])

        outputarray.append(dp)

    return outputarray

answer = median_filter(testdata)

for i in range(0,len(answer)):
    print(answer[i].print_values())
