import os
import cv2
import numpy as np
from math import sin, cos, radians
import datetime
import time
import calendar
from statistics import median
from PIL import Image
from plotly import graph_objects as go

# # offset values when coronagraph mask support-vane in top-right position
# offset_x = -5
# offset_y = 10

# offset values when coronagraph mask support-vane in bottom-left position
offset_x = 5
offset_y = -10

image_size = 512
imagecentre = image_size / 2

# Parameters for CME detection
cme_min = 0.4
cme_partial = 0.6
cme_halo = 0.8


def create_gif(list, filesfolder):
    imagelist = []
    for item in list:
        j = filesfolder + "/" + item
        i = Image.open(j)
        imagelist.append(i)
    imagelist[0].save("cme.gif",
                      format="GIF",
                      save_all=True,
                      append_images=imagelist[1:],
                      duration=500,
                      loop=0)


def median_filter(data):
    # simple 3 value median filter
    filtered = []
    t = []
    for item in data:
        t.append(float(item))
        if len(t) == 3:
            f = median(t)
            filtered.append(f)
            t.pop(0)
    return filtered


def plot_mini(dates, pixel_count):
    savefile = "cme_mini.jpg"
    # pixel_count = median_filter(pixel_count)
    dates.pop(0)
    dates.pop(len(dates) - 1)
    red = "rgba(150, 0, 0, 1)"
    green = "rgba(0, 150, 0, 0.8)"
    orange = "rgba(150, 100, 0, 0.8)"

    plotdata = go.Scatter(x=dates, y=pixel_count, mode="lines")
    fig = go.Figure(plotdata)

    fig.update_layout(font=dict(size=20), title_font_size=24)
    fig.update_layout(title="Coronal Mass Ejections",
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>",
                      yaxis_title="CME Coverage",
                      plot_bgcolor="#e0e0e0")
    fig.update_layout(plot_bgcolor="#a0a0a0", paper_bgcolor="#a0a0a0")

    # fig.update_xaxes(nticks=50, tickangle=45)
    fig.update_yaxes(range=[0, 1.01])

    fig.add_hline(y=cme_min, line_color=green, line_width=6, annotation_text="Minor CME",
                  annotation_font_color="darkslategrey", annotation_font_size=20, annotation_position="top left")

    fig.add_hline(y=cme_partial, line_color=orange, line_width=6, annotation_text="Partial Halo CME",
                  annotation_font_color="darkslategrey", annotation_font_size=20, annotation_position="top left")

    fig.add_hline(y=1, line_color=red, line_width=6, annotation_text="Full Halo CME",
                  annotation_font_color="darkslategrey", annotation_font_size=20, annotation_position="top left")
    fig.update_traces(line=dict(width=4, color=red))
    fig.write_image(file=savefile, format='jpg')


def plot(dates, pixel_count, filename, width, height):
    savefile = filename
    pixel_count = median_filter(pixel_count)
    dates.pop(0)
    dates.pop(len(dates) - 1)
    red = "rgba(150, 0, 0, 1)"
    green = "rgba(0, 150, 0, 0.8)"
    orange = "rgba(150, 100, 0, 0.8)"

    plotdata = go.Scatter(x=dates, y=pixel_count, mode="lines")
    fig = go.Figure(plotdata)

    fig.update_layout(font=dict(size=20), title_font_size=21)
    fig.update_layout(width=width, height=height, title="Coronal Mass Ejections",
                      xaxis_title="Date/time UTC<br><sub>http://DunedinAurora.nz</sub>",
                      yaxis_title="CME Coverage",
                      plot_bgcolor="#e0e0e0")
    fig.update_layout(plot_bgcolor="#a0a0a0", paper_bgcolor="#a0a0a0")

    fig.update_xaxes(nticks=25, tickangle=45)
    fig.update_yaxes(range=[0, 1.01])

    fig.add_hline(y=cme_min, line_color=green, line_width=6, annotation_text="Minor CME",
                  annotation_font_color=green, annotation_font_size=20, annotation_position="top left")

    fig.add_hline(y=cme_partial, line_color=orange, line_width=6, annotation_text="Partial Halo CME",
                  annotation_font_color=orange, annotation_font_size=20, annotation_position="top left")

    fig.add_hline(y=1, line_color=red, line_width=6, annotation_text="Full Halo CME",
                  annotation_font_color=red, annotation_font_size=20, annotation_position="top left")
    fig.update_traces(line=dict(width=4, color=red))
    fig.write_image(file=savefile, format='jpg')


def annotate_image(array, width, height, timevalue):
    #  downconvert image
    cimage = np.array(array, np.uint16)
    cimage = cv2.cvtColor(cimage, cv2.COLOR_GRAY2BGR)

    rad_sol = 10  # solar radius in pixels at 512 pixels
    north = 0
    east = 90
    south = 180
    west = 270

    # NSWE lines
    cv2.line(cimage, (north, 0), (north, height), (0, 100, 255), thickness=1)
    cv2.line(cimage, (east, 0), (east, height), (0, 100, 255), thickness=1)
    cv2.line(cimage, (south, 0), (south, height), (0, 100, 255), thickness=1)
    cv2.line(cimage, (west, 0), (west, height), (0, 100, 255), thickness=1)
    # solar surface
    cv2. rectangle(cimage, (0, height - rad_sol), (width, height), (0, 255, 255), -1)
    cv2.rectangle(cimage, (0, 0), (width, 12), (0, 0, 0), -1)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 0.4
    font_color = (0, 100, 255)
    font_thickness = 1
    cv2.putText(cimage, "N", (north, 10), font, font_size, font_color, font_thickness, cv2.LINE_AA)
    cv2.putText(cimage, "E", (east, 10), font, font_size, font_color, font_thickness, cv2.LINE_AA)
    cv2.putText(cimage, "S", (south, 10), font, font_size, font_color, font_thickness, cv2.LINE_AA)
    cv2.putText(cimage, "W", (west, 10), font, font_size, font_color, font_thickness, cv2.LINE_AA)

    font_color = (0, 255, 255)
    cv2.putText(cimage, "Solar Surface", (10, height - 15), font, font_size, font_color, font_thickness, cv2.LINE_AA)
    cv2.putText(cimage, timevalue, (220, height - 15), font, font_size, font_color, font_thickness, cv2.LINE_AA)
    # THis box marks the slot used to detect count pixels for CMEs
    cv2.rectangle(cimage, (0, 220 - 50), (359, 220 - 40), (0, 255, 0), 1)
    return cimage


def text_alert(px, hr):
    # %Y-%m-%d %H:%M
    cme_detect = False
    timestring = hr
    hr = hr.split(" ")
    hr = hr[0]
    hr = hr.split("-")
    new_hr = hr[0] + "/" + hr[1] + "/" + hr[2]
    url = "https://stereo-ssc.nascom.nasa.gov/browse/" + new_hr +  "/ahead/cor2_rdiff/512/thumbnail.shtml"
    stereo_url = "<a href=\"" + url + "\" target=\"_blank\">" + "Stereo Science Centre</a>"
    savefile = "cme_alert.php"
    msg = "<p>No significant activity detected in the last 24 hours."
    heading = "<b>CME Monitor updated at " + posix2utc(time.time(), " %Y-%m-%d %H:%M") + " UTC.</b>"
    if px > cme_min:
        cme_detect = True
        msg = "<p>A possible CME has been detected at " + timestring +  " with " + str(int(px * 100)) + "% coverage."
        if px >= cme_partial:
            cme_detect = True
            msg = "<p>Warning: A possible PARTIAL HALO CME has been detected  at " + timestring +  " with " + str(int(px * 100)) + "% coverage."
            if px >= cme_halo:
                cme_detect = True
                msg = "<p>ALERT: A possible FULL HALO CME has been detected at " + timestring +  " with " + str(int(px * 100)) + "% coverage."

    if cme_detect == True:
        msg = msg + "<br>Confirm Earth impact with STEREO A satellite data: " + stereo_url

    msg_alert = heading + msg
    with open(savefile, "w") as s:
        s.write(msg_alert)
    s.close()


def filehour_converter(yyyymmdd, hhmm):
    year = (yyyymmdd[:4])
    month = (yyyymmdd[4:6])
    day = (yyyymmdd[6:])
    hour = (hhmm[:2])
    min = (hhmm[2:])
    utc_string = year + '-' + month + '-' + day + ' ' + hour + ':' + min
    dt = datetime.datetime.strptime(utc_string, '%Y-%m-%d %H:%M')
    ts = calendar.timegm(dt.timetuple())
    return ts


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def count_nonzero(array):
    # COunt non zero pixels in a zone just above the solar surface.
    try:
        num_pixels = cv2.countNonZero(array)
    except Exception:
        num_pixels = 0
    return num_pixels


def create_mask(image, imagewidth, imageheight, topoffset, bottomoffset):
    mask = np.zeros(image.shape[:2], dtype="float64")
    cv2.rectangle(mask, (0, imageheight - topoffset), (imagewidth, imageheight - bottomoffset), 255, -1)
    return mask


def polar_to_rectangular(angle, distance):
    """
    With our image, we have a line at an angle , radiating from
    the centre. We want the pixel value at the end. THis method will return the [x,y] co-ords accounting
    for the offset the actual centre point from the geometric centre of the image

    Angle: in degrees measured clockwise from North/top
    Distance: in pixels, as a radius measured from the centre.
    """
    if angle == 0 or angle == 360:
        # print("a == 0")
        x = imagecentre
        y = imagecentre - distance

    if angle > 0:
        if angle < 90:
            # print("0 < a < 90")
            delta_x = distance * sin(radians(angle))
            delta_y = distance * cos(radians(angle))
            x = imagecentre + delta_x
            y = imagecentre - delta_y

    if angle == 90:
        # print("a == 90")
        x = imagecentre + distance
        y = imagecentre

    if angle > 90:
        if angle < 180:
            # print("90 < a < 180")
            angle = angle - 90
            delta_y = distance * sin(radians(angle))
            delta_x = distance * cos(radians(angle))
            x = imagecentre + delta_x
            y = imagecentre + delta_y

    if angle == 180:
        # print("a == 180")
        x = imagecentre
        y = imagecentre + distance

    if angle > 180:
        if angle < 270:
            # print("180 < a < 270")
            angle = angle - 180
            delta_x = distance * sin(radians(angle))
            delta_y = distance * cos(radians(angle))
            x = imagecentre - delta_x
            y = imagecentre + delta_y

    if angle == 270:
        # print("a == 270")
        x = imagecentre - distance
        y = imagecentre

    if angle > 270:
        if angle < 360:
            # print("270 < a < 360")
            angle = angle - 270
            delta_y = distance * sin(radians(angle))
            delta_x = distance * cos(radians(angle))
            x = imagecentre - delta_x
            y = imagecentre - delta_y

    # finally add the offsets and return
    x = int(x + offset_x)
    y = int(y + offset_y)
    return [x, y]


def log_errors(errormessage):
    print(errormessage)


def image_load(file_name):
    # Return a None if the image is currupt
    try:
        pil_image = Image.open(file_name)
        # pil_image.verify()
        pil_image.transpose(Image.FLIP_LEFT_RIGHT)
        pil_image.close()
        img = cv2.imread(file_name)
    except Exception as e:
        print(e)
        img = None

    return img


def image_save(file_name, image_object):
    cv2.imwrite(file_name, image_object)


def greyscale_img(image_to_process):
    # converting an Image to grey scale one channel...
    greyimg = cv2.cvtColor(image_to_process, cv2.COLOR_BGR2GRAY, 1)
    return greyimg


def wrapper(storage_folder, analysis_folder):
    # get a list of the current stored images.
    dirlisting = os.listdir(storage_folder)

    # make sure they are in chronological order by name
    dirlisting.sort()

    avg_array = []
    pixel_count = []
    dates = []
    px_max = cme_min
    px_date = posix2utc((time.time() - 86400), "%Y-%m-%d %H:%M")

    for i in range (0, len(dirlisting)):
        p = storage_folder + "//" + dirlisting[i]

        # Test that image is not corrupted

        img = image_load(p)

        if img is not None:
            img_g = greyscale_img(img)
            kernel1 = np.ones((3, 3), np.uint8)
            # Create an array of pictures with which to create an average
            # that is isued to compare individual images, essentiall a 3D version
            #  of finding the residual.
            # Pic is used for comparisons and must be float64
            pic = cv2.erode(img_g, kernel1, iterations=1)
            pic = np.array(pic, np.float64)
            avg_array.append(pic)

            # 100 images is about a day. Start comparing individual images against an "average" image
            if len(avg_array) >= 100:
                # ALWAYS POP
                avg_array.pop(0)
                avg_img = np.mean(avg_array, axis=0)
                detrended_img = cv2.subtract(pic, avg_img)
                ret, detrended_img = cv2.threshold(detrended_img, 3, 255, cv2.THRESH_BINARY)

                #  convolve the returned residuals image from polar to rectangular co-ords. the data is appended to
                #  an array
                radius = 220
                angle = 360
                t = []
                for j in range(radius, 0, -1):
                    for k in range(0, angle):
                        coords = polar_to_rectangular(k, j)
                        pixelvalue = detrended_img[coords[1], coords[0]]
                        t.append(pixelvalue)

                # Convert the 1D array into a 2D image
                array = np.reshape(np.array(t), (radius, angle))
                #  Just crops the image
                mask = create_mask(array, angle, radius, 40, 50)
                masked = cv2.bitwise_and(array, mask)

                # Pixelcounter to create graphic pf CMEs
                # A full halo CME should produce counts in the order of 3600
                px = count_nonzero(masked)

                #  pixelcount as a percentage of the area monitored
                px = float(px) / 3600
                px = round(px, 3)
                t = dirlisting[i].split("_")
                posixtime = filehour_converter(t[0], t[1])
                hr = posix2utc(posixtime, "%Y-%m-%d %H:%M")
                # text_alert(px, hr)

                #  For text alerts, CME in the last day
                if px >= px_max:
                    if posixtime > (time.time() - 86400):
                        px_max = px
                        px_date =  hr

                pixel_count.append(px)
                dates.append(hr)
                # Annotate image for display
                array = annotate_image(array, angle, radius, hr)

                f_image = analysis_folder + "//" + "dt_" + dirlisting[i]
                image_save(f_image, array)

                print("dt", i, len(dirlisting))
        else:
            msg = "Unable to load picure " + p
            log_errors(msg)

    # #  Creat text alert
    text_alert(px_max, px_date)

    # Create line graphs of CME detections
    print(len(dates), len(pixel_count))
    pixel_count = median_filter(pixel_count)
    dates.pop(len(dates) - 1)
    dates.pop(0)
    plot(dates, pixel_count, "cme_plot.jpg", 1800, 600)

    dates = dates[-100:]
    pixel_count = pixel_count[-100:]
    plot_mini(dates, pixel_count)

    # create an animated GIF of the last 24 images from the Analysis folder.
    imagelist = os.listdir(analysis_folder)
    imagelist.sort()
    listlength = 100
    if len(imagelist) > listlength:
        cut = len(imagelist) - listlength
        imagelist = imagelist[cut:]
    imagelist.sort()
    print("creating animated GIF...")

    create_gif(imagelist, analysis_folder)