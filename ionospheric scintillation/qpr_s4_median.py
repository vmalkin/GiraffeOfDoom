# create a graph of the median S4 values for each time bin
# Typically I would create preset bin objects for each time interval and populate an array in each
# object and use the median value of that array. THis time I'm just going to compare the current and next datetimes
# for each entry in the query and act on that.

# dependencies include Plotly, Kaleido, Pandas

from statistics import median, mean
import datetime
import plotly.graph_objects as go
import constants as k

timeformat = '%Y-%m-%d %H:%M'

def save_s4(filename, data):
    try:
        with open(filename, 'w') as f:
            f.write("Datetime UTC, Median S4 Index" + '\n')
            for result in data:
                f.write(result + '\n')
        f.close()
        print("Median S4 csv file written")
    except PermissionError:
        print("CSV file being used by another app. Update next time")


def posix2utc(posixtime):
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime

def plot_lineplot(xval, yval):
    savefile = k.imagesdir + "//avg.jpg"
    data = go.Scatter(x=xval, y = yval, mode="lines")
    fig = go.Figure(data)
    fig.update_yaxes(range=[1, 40], gridcolor='#505050')
    fig.update_xaxes(nticks=24, tickangle=45, gridcolor='#505050')
    fig.update_layout(width=1700, height=600, title="S4 Avg Index, GPS & Glonass Constellations. http://DunedinAurora.NZ", xaxis_title="Date/time UTC", yaxis_title="S4 Index", plot_bgcolor="#101010")
    fig.update_traces(line=dict(width=2, color="rgba(0,255,255,0.5)"))
    fig.write_image(file=savefile, format='jpg')
    # fig.show()


# query format:
# ('satID', posixtime, alt, az, s4, snr)
def wrapper(queryresults):
    finallist = []
    tempvalues = []
    xval = []
    yval = []

    # make the end one less the length of the query so we dont get index errors
    for i in range(0, len(queryresults) - 1):
        now_dt = queryresults[i][1]
        next_dt = queryresults[i + 1][1]
        value = queryresults[i][4]
        if next_dt == now_dt:
            tempvalues.append(value)

        if next_dt > now_dt:
            medvalue = median(tempvalues)
            dp = posix2utc(now_dt) + "," + str(medvalue)
            finallist.append(dp)
            xval.append(posix2utc(now_dt))
            yval.append(medvalue)
            tempvalues = []

    save_s4("s4_median.csv", finallist)
    plot_lineplot(xval, yval)



