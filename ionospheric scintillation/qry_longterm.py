import datetime
import constants as k
import plotly.graph_objects as go
import mgr_stats
import sqlite3
import time

sat_database = "gps_satellites.db"
optimum_altitude = 25

def plot(ut, da):
    savefile = k.imagesdir + "//longterm.svg"
    clr_grid = '#c7c7c7'
    data = go.Scatter(x=ut, y = da, mode="lines")
    fig = go.Figure(data)
    # fig.update_yaxes(range=[170, 210], gridcolor=clr_grid)
    max_d = max(da) + 5
    min_d = min(da) - 5

    fig.update_yaxes(range=[min_d, max_d], gridcolor=clr_grid)

    # clr_mean = "rgba(200,10,10,0.8)"
    # clr_sigma = "rgba(0,150,0,0.8)"
    # fig.add_hline(y=median, line_color=clr_mean, annotation_text="x ̅", annotation_font_color=clr_mean, annotation_position="top left")
    # fig.add_hline(y=(median + sigma*2), line_color=clr_sigma, annotation_text="2σ",annotation_font_color=clr_sigma, annotation_position="top left")
    # fig.add_hline(y=(median + sigma*4), line_color=clr_sigma, annotation_text="4σ", annotation_font_color=clr_sigma, annotation_position="top left")
    # fig.add_hline(y=(median + sigma*6), line_color=clr_sigma, annotation_text="6σ", annotation_font_color=clr_sigma, annotation_position="top left")

    fig.update_xaxes(nticks=24, tickangle=45, gridcolor=clr_grid)
    fig.update_layout(font=dict(size=20), title_font_size=21)
    fig.update_layout(width=1700, height=700, title="Rolling 24hr count GPS noise. s4 > 40. http://DunedinAurora.NZ", xaxis_title="Date/time UTC", yaxis_title="S4 Index", plot_bgcolor="#e0e0e0")
    fig.update_traces(line=dict(width=2, color="rgba(10,10,10,1)"))
    fig.write_image(file=savefile, format='svg')
    fig.show()


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def database_parse(hourduration):
    starttime = int(time.time()) - (60 * 60 * hourduration)
    print("Parsing database...")
    gpsdb = sqlite3.connect(sat_database)
    db = gpsdb.cursor()

    result = db.execute('select sat_id, posixtime, alt, az, s4, snr from satdata where posixtime > ? and alt > ? order by posixtime asc', [starttime, optimum_altitude])
    returnlist = []
    for item in result:
        dp = (item[0], item[1], item[2], item[3], item[4], item[5])
        returnlist.append(dp)
    print("current query " + str(len(returnlist)) + " records long")
    gpsdb.commit()
    db.close()
    return returnlist


# query format:
# ('satID', posixtime, alt, az, s4, snr)
# Query is 48 hours of data, each datapoint is one minute for a different satellite
def wrapper(querydata):
    s4_threshold = 40
    s4_altitude = 40
    firstpass_utc = []
    firstpass_dat = []
    minute_count = 0

    #  We are just counting instances of an S4 reading being over our threshold, if so, bump the counter for tha min
    for i in range(0, len(querydata)-1):
        min_now = querydata[i][1]
        min_next = querydata[i+1][1]
        s_alt = querydata[i][2]
        s_s4 = querydata[i][4]
        if min_now == min_next:
            if s_alt >= s4_altitude:
                if s_s4 >= s4_threshold:
                    minute_count = minute_count + 1
        # we've finished the minute, append the total, the we'll count the next minute.
        else:
            firstpass_dat.append(minute_count)
            firstpass_utc.append(posix2utc(min_now, '%Y-%m-%d %H:%M'))
            minute_count = 0

    lastpass_dat = []
    lastpass_utc = []
    rolling = []

    # We build up our temp array rolling until it is a day long, then we get the cumulative sum, add the sum to the
    # output list.
    for j in range(0, len(firstpass_dat)):
        if len(rolling) < 1440:
            rolling.append(firstpass_dat[j])
        else:
            rolling.pop(0)
            rolling.append(firstpass_dat[j])
            dp = sum(rolling)
            dt = firstpass_utc[j]
            lastpass_dat.append(dp)
            lastpass_utc.append(dt)

    plot(lastpass_utc, lastpass_dat)
    print("Plot complete")


t = 24 * 60
qry = database_parse(t)
wrapper(qry)