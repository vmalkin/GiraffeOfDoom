import glob
import os
import cv2
import numpy as np
from plotly import graph_objects as go
# file path seperator / or \ ???
pathsep = os.sep


def create_mask(image):
    # Mask off the outer corona and only focus on the image of the sun
    diameter_ratio = 380 / 1280
    width, height, colourdepth = image.shape
    solar_diameter = int(diameter_ratio * width)
    mask = np.zeros((width, height), dtype=np.int8)
    x_offset = 0
    y_offset = 0
    x_centre = int(width / 2) + x_offset
    y_centre = int(height / 2) + y_offset
    cv2.circle(mask, (x_centre, y_centre), solar_diameter, (255,255,255), -1)
    image = cv2.bitwise_and(image, image, mask=mask)
    return image


def local_file_list_build(directory):
    # Builds and returns a list of files contained in the directory.
    # List is sorted into A --> Z order
    dirlisting = []
    path = directory + pathsep + "*.*"
    for name in glob.glob(path):
        name = os.path.normpath(name)
        dirlisting.append(name)
    dirlisting.sort()
    return dirlisting


def getfilename(pathname):
    p = pathname.split(pathsep)
    pp = p[1].split('_')
    return pp[0]


def plot(event_data):
    fig = go.Figure()
    for data in event_data:
        # Each data is is an array [datetime, data1, data2]
        dt = []
        d0 = []
        d1 = []
        for entries in data:
            dt.append(entries[0])
            d0.append(entries[1])
            d1.append(entries[2])
        fig.add_bar(x=dt, y=d0)
        fig.add_bar(x=dt, y=d1)
        # Force y axis to show at least 10
        fig.update_yaxes(range=[10, None])
    fig.update_layout(barmode='group')
    fig.show()

def wrapper():
    print('*** Begin Histogram Analysis')

    # Supply a list of sub folders with diffs images in them to analyse
    folders = ['diffs_g', 'diffs_b', 'diffs_r']
    solar_surface_events = []

    for folder in folders:
        img_files = local_file_list_build(folder)
        # a day is roughly 360 images
        img_files = img_files[-360:]

        returnarray = []
        for item in img_files:
            tmp = []
            img = cv2.imread(item)
            # Mask off the outer corona - we're only interested in the solar disc
            img = create_mask(img)

            result = np.histogram(img, bins=5, range=(0, 256))
            # result[0] is histogram, result[1] are bin labels
            histgm = (result[0])

            tmp.append(getfilename(item))
            tmp.append(histgm[0])
            tmp.append(histgm[4])
            # for item in histgm:
            #     tmp.append(item)
            returnarray.append(tmp)

        px_white = []
        px_black = []
        dates = []
        for item in returnarray:
            dates.append(item[0])
            px_white.append(item[1])
            px_black.append(item[2])

        avg_white = np.average(px_white)
        std_white = np.std(px_white)
        avg_black = np.average(px_black)
        std_black = np.std(px_black)

        events = []
        for i in range(0, len(dates)):
            dt = dates[i]
            # href=''
            if px_white[i] > (avg_white + std_white):
                cme_wh = round(((px_white[i] - avg_white) / std_white), 3)
            else:
                cme_wh = 0

            if px_black[i] > (avg_black + std_black):
                cme_bl = round(((px_black[i] - avg_black) / std_black), 3)
            else:
                cme_bl = 0

            line = [dt, cme_wh, cme_bl]
            events.append(line)
        solar_surface_events.append(events)

    plot(solar_surface_events)
    print('*** End Histogram Analysis')
