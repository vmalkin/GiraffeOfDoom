import mgr_daily_count

import sqlite3
import time
import datetime
from plotly import graph_objects as go

database = "events.db"


def database_get_data(hours_duration):
    duration = hours_duration * 3600
    tempdata = []
    starttime = int(time.time()) - duration
    db = sqlite3.connect(database)
    cursor = db.cursor()
    result = cursor.execute("select posixtime from data where posixtime > ? order by posixtime asc", [starttime])
    for line in result:
        d = line[0]
        tempdata.append(d)
    db.close()
    return tempdata


def plot(dates, data):
    fig = go.Figure(go.Bar(x=dates, y=data,
                           marker=dict(color='#340059', line=dict(width=0.5, color='#340059'))))
    fig.update_xaxes(ticks='outside', tickangle=45)
    # fig.update_yaxes(range=[0, 1],  nticks=2)
    fig.update_layout(font=dict(size=14), title_font_size=21)
    fig.update_layout(plot_bgcolor="#a0a0a0", paper_bgcolor="#a0a0a0")
    fig.update_layout(width=1400, height=600,
                      title="Muons - Daily count",
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>")
    # title = "muons_avg_" + str(hrs) + "_hr.jpg"
    fig.write_image("muon_daily.jpg")


data = database_get_data(24 * 7)
try:
    mgr_daily_count.wrapper()
except:
    print("Failed to print cumulative totals")