import datetime
import constants as k
import plotly.graph_objects as go


def plot(ut, da):
    savefile = k.imagesdir + "//cumulative.jpg"
    data = go.Scatter(x=ut, y = da, mode="lines")
    fig = go.Figure(data)
    # fig.update_yaxes(range=[120, 180], gridcolor='#505050')
    fig.update_yaxes(range=[60, 100], gridcolor='#505050')
    fig.update_xaxes(nticks=24, tickangle=45, gridcolor='#505050')
    fig.update_layout(font=dict(size=22), title_font_size=22)
    fig.update_layout(width=1700, height=700, title="Rolling 24hr count GPS Noise. http://DunedinAurora.NZ", xaxis_title="Date/time UTC", yaxis_title="S4 Index", plot_bgcolor="#101010")
    fig.update_traces(line=dict(width=2, color="rgba(0,255,255,0.8)"))
    fig.write_image(file=savefile, format='jpg')


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


# query format:
# ('satID', posixtime, alt, az, s4, snr)
# Query is 48 hours of data, each datapoint is one minute for a different satellite
def wrapper(querydata):
    s4_threshold = 40
    s4_altitude = 40
    firstpass_utc = []
    firstpass_dat = []
    minute_count = 0

    for i in range(0, len(querydata)-1):
        min_now = querydata[i][1]
        min_next = querydata[i+1][1]
        s_alt = querydata[i][2]
        s_s4 = querydata[i][4]
        if min_now == min_next:
            if s_alt >= s4_altitude:
                if s_s4 >= s4_threshold:
                    minute_count = minute_count + 1
        else:
            firstpass_dat.append(minute_count)
            firstpass_utc.append(posix2utc(min_now, '%Y-%m-%d %H:%M'))
            minute_count = 0

    lastpass_dat = []
    lastpass_utc = []
    rolling = []

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


