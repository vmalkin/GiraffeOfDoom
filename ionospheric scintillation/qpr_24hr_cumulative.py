import datetime
import constants as k
import plotly.graph_objects as go
# import mgr_stats


def plot(ut, da, median, sigma):
    savefile = k.imagesdir + "//cumulative.jpg"
    clr_grid = '#c7c7c7'
    data = go.Scatter(x=ut, y = da, mode="lines")
    fig = go.Figure(data)
    # fig.update_yaxes(range=[170, 210], gridcolor=clr_grid)
    max_d = max(da) + 5
    min_d = min(da) - 5

    fig.update_yaxes(range=[min_d, max_d], gridcolor=clr_grid)

    clr_mean = "rgba(200,10,10,0.8)"
    clr_upsigma = "rgba(0,150,0,0.8)"
    clr_downsigma = "rgba(0,0,150,0.8)"
    fig.add_hline(y=median, line_color=clr_mean, line_width=1, annotation_text="x", annotation_font_color=clr_mean, annotation_position="top left")
    fig.add_hline(y=(median + sigma*2), line_color=clr_upsigma, line_width=2, annotation_text="2σ",annotation_font_color=clr_upsigma, annotation_position="top left")
    fig.add_hline(y=(median + sigma*4), line_color=clr_upsigma, line_width=4, annotation_text="4σ", annotation_font_color=clr_upsigma, annotation_position="top left")
    fig.add_hline(y=(median + sigma*6), line_color=clr_upsigma, line_width=6,annotation_text="6σ", annotation_font_color=clr_upsigma, annotation_position="top left")
    fig.add_hline(y=(median - sigma * 2), line_color=clr_downsigma,  line_width=2, annotation_text="-2σ", annotation_font_color=clr_downsigma, annotation_position="bottom left")
    fig.add_hline(y=(median - sigma * 4), line_color=clr_downsigma,  line_width=4, annotation_text="-4σ", annotation_font_color=clr_downsigma, annotation_position="bottom left")
    fig.add_hline(y=(median - sigma * 6), line_color=clr_downsigma,  line_width=6, annotation_text="-6σ", annotation_font_color=clr_downsigma, annotation_position="bottom left")

    fig.update_xaxes(nticks=24, tickangle=45, gridcolor=clr_grid)
    fig.update_layout(font=dict(size=20), title_font_size=21)
    fig.update_layout(width=1700, height=700, title="Rolling 24hr count GPS noise. s4 > 40. http://DunedinAurora.NZ", xaxis_title="Date/time UTC", yaxis_title="Count S4 events", plot_bgcolor="#e0e0e0")
    fig.update_traces(line=dict(width=5, color="rgba(10,10,10,1)"))
    fig.write_image(file=savefile, format='jpg')


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


# query format:
# ('satID', posixtime, alt, az, s4, snr)
# Query is 48 hours of data, each datapoint is one minute for a different satellite
def wrapper(querydata, statvalues):
    s4_threshold = 40
    s4_altitude = 40
    firstpass_utc = []
    firstpass_dat = []
    minute_count = 0

    #  We are just counting instances of an S4 reading being over our threshold, if so, bump the counter for tha min
    # S4 values must be less that 100.
    for i in range(0, len(querydata)-1):
        min_now = querydata[i][1]
        min_next = querydata[i+1][1]
        s_alt = querydata[i][2]
        s_s4 = querydata[i][4]
        if min_now == min_next:
            if s_alt >= s4_altitude:
                if s_s4 >= s4_threshold and s_s4 < 100:
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

    plot(lastpass_utc, lastpass_dat, statvalues["medianvalue"], statvalues["mediansigma"])
    print("Plot complete")


