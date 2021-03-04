from time import time
import plotly.graph_objects as go


def plot():
    pass


# query format:
# ('satID', posixtime, alt, az, s4, snr)
# Query is 48 hours of data
def wrapper(querydata):
    time_start = time()
    s4_threshold = 40
    s4_altitude = 40
    utc = []
    dat = []

# get 24 hr of data from start of array, then...
# sum up S4, save to temp list, save timestamp.
# pop(0), move along one and append(newvalue), repeat!
