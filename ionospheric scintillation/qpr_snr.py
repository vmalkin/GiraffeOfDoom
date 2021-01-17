"""
To create simple scatterplot of S4 data
dependencies include Plotly, Kaleido, Pandas
"""
import datetime
import plotly.express as px

timeformat = '%Y-%m-%d %H:%M'

def posix2utc(posixtime):
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def plot_scatterplot(xvalues, yvalues):
    fig = px.scatter(x=xvalues, y=yvalues, title = 'S/N Ratio - Satellite Constellaton')
    fig.write_image(file='snr.jpg', format='jpg')
    # fig.show()


# query format:
# ('satID', posixtime, alt, az, s4, snr)
def wrapper(queryresults):
    xval = []
    yval = []
    for item in queryresults:
        dt = item[1]
        dt = posix2utc(dt)
        da = item[5]

        xval.append(dt)
        yval.append(da)

    plot_scatterplot(xval, yval)