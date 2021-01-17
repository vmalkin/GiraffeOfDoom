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


def save_s4(filename, data):
    try:
        with open(filename, 'w') as f:
            f.write("Datetime UTC, S4 Scintillation Index" + '\n')
            for result in data:
                f.write(result + '\n')
        f.close()
        print("S4 csv"
              " file written")
    except PermissionError:
        print("CSV file being used by another app. Update next time")


def plot_scatterplot(xvalues, yvalues):
    fig = px.scatter(x=xvalues, y=yvalues, title = 'S4 Index')
    fig.write_image(file='scatter.jpg', format='jpg')
    # fig.show()

# query format:
# ('satID', posixtime, alt, az, s4, snr)
def wrapper(queryresults):
    datalist = []
    xval = []
    yval = []
    for item in queryresults:
        dt = item[1]
        dt = posix2utc(dt)
        da = item[4]

        xval.append(dt)
        yval.append(da)

        dp = dt + "," + str(da)
        datalist.append(dp)

    save_s4("s4.csv", datalist)
    plot_scatterplot(xval, yval)