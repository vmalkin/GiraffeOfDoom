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
import standard_stuff
import glob

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


def process_columns(image):
# takes a cropped image. Determins a value for each column in the image.
# A CME should appear as a surge in brighness across several connected columns that
# changes with time.
# Streamers are ever present, but although contiguous, change far more slowly
    returnarray = []
    img = np.array(image)
    array_length = image.shape[1]
    for i in range(0, array_length):
        column_sum = sum(img[:,i])
        returnarray.append(column_sum)
    return returnarray


def create_gif(list, filesfolder, gif_name):
    imagelist = []
    for item in list:
        j = filesfolder + "/" + item
        i = Image.open(j)
        imagelist.append(i)
    imagelist[0].save(gif_name,
                      format="GIF",
                      save_all=True,
                      append_images=imagelist[1:],
                      duration=500,
                      loop=0)


def create_video(list, filesfolder, video_name):
    imagelist = []
    for item in list:
        j = filesfolder + "/" + item
        i = cv2.imread(j)
        imagelist.append(i)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(video_name, fourcc, 4, (360, 220))

    for item in imagelist:
        video.write(item)
    video.release()


def median_filter(data):
    # simple 3 value median filter
    filtered = []
    t = []
    for item in data:
        t.append(float(item))
        if len(t) == 5:
            f = median(t)
            filtered.append(f)
            t.pop(0)
    return filtered


def plot_diffs_polar(pixel_count, filename, width, height):
    savefile = filename
    colourstep = int(round(255 / len(pixel_count), 0))
    papercolour = "#303030"

    theta = []
    for i in range(0, len(pixel_count[0])):
        j = i / len(pixel_count[0]) * 360
        theta.append(j)
    theta.append(0)

    x_step = -0.02
    x1_step = 0.00
    fig = go.Figure()
    for i in range(0, len(pixel_count)):
        j = colourstep * i
        linecolour = "rgba(" + str(j) + ", 0," + str(255 - j) + ", 1)"
        fig.add_shape(type="rect", xref="paper", yref="paper", x0=x_step, y0=-0.04, x1=x1_step, y1=-0.02,
                      line=dict(color=linecolour),
                      fillcolor=linecolour)
        fig.add_trace(go.Scatterpolar(
            r=pixel_count[i],
            theta=theta,
            mode="lines",
            line_color=linecolour))

        if i == len(pixel_count) - 1:
            fig.add_shape(type="rect", xref="paper", yref="paper", x0=x_step, y0=-0.04, x1=x1_step, y1=-0.02,
                          line=dict(color="yellow"),
                          fillcolor="yellow")
            fig.add_trace(go.Scatterpolar(
                r=pixel_count[i],
                theta=theta,
                mode="lines",
                line_color="#ffff00"))
        x_step = x_step + 0.009
        x1_step = x1_step + 0.009

    # The Sun
    sun_x = int(width / 2) - 80
    sun_y = int(height / 2) - 90
    fig.add_shape(
        type="circle",
        # xref="x", yref="y",
        xsizemode="pixel", ysizemode="pixel",
        xanchor=0, yanchor=0,
        x0=sun_x - 50, y0=sun_y - 50,
        x1=sun_x + 50, y1=sun_y + 50,
        fillcolor="gold")

    fig.update_layout(font=dict(size=20, color="#e0e0e0"), title_font_size=21)
    fig.update_layout(paper_bgcolor=papercolour)
    fig.update_layout(showlegend=False, width=width, height=height,
                      title="Solar Corona - 24 Hrs - Brightness and Azimuth")

    fig.add_annotation(text="24 Hours ago", x=0.1, y=-0.03)
    fig.add_annotation(text="NOW", x=1.03, y=-0.03)

    fig.update_polars(
        hole=0.2,
        bgcolor="#000000",
        angularaxis_linecolor=papercolour,
        angularaxis_direction="clockwise",
        angularaxis_rotation=90,
        angularaxis_gridwidth=4,
        angularaxis_gridcolor=papercolour,
        radialaxis_gridwidth=4,
        radialaxis_gridcolor=papercolour,
        radialaxis_showticklabels=True,
        radialaxis_color="white",
        radialaxis_linewidth=3,
        radialaxis=dict(angle=90),
        radialaxis_tickangle=90
    )
    fig.write_image(file=savefile, format='jpg')


def plot_diffs(pixel_count, filename, width, height):
    savefile = filename
    plotdata = go.Scatter(mode="lines")
    fig = go.Figure(plotdata)
    colourstep = int(round(255 / len(pixel_count), 0))
    verticalstep = int(len(pixel_count[0]) / 4)

    for i in range(0, len(pixel_count)):
        j = colourstep * i
        # linecolour = "rgba(" + str(255 - i) + ", " + str(40 + i) + ", 0, 1)"
        linecolour = "rgba(" + str(j) + ", 0," + str(255 - j) + ", 1)"
        fig.add_trace(go.Scatter(y=pixel_count[i], mode="lines", line=dict(color=linecolour, width=2)))
        if i == len(pixel_count) - 1:
            fig.add_trace(go.Scatter(y=pixel_count[i], mode="lines", line=dict(color="#ffff00", width=2)))

    fig.update_xaxes(showgrid=False, showticklabels=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#505050')

    ll = "#909090"
    fig.add_vline(x=0, line_color=ll, line_width=3, annotation_text="North",
                  annotation_font_color=ll, annotation_font_size=20, annotation_position="top right")
    fig.add_vline(x=verticalstep, line_color=ll, line_width=3, annotation_text="East",
                  annotation_font_color=ll, annotation_font_size=20, annotation_position="top right")
    fig.add_vline(x=verticalstep * 2, line_color=ll, line_width=3, annotation_text="South",
                  annotation_font_color=ll, annotation_font_size=20, annotation_position="top right")
    fig.add_vline(x=verticalstep * 3, line_color=ll, line_width=3, annotation_text="West",
                  annotation_font_color=ll, annotation_font_size=20, annotation_position="top right")

    fig.update_layout(font=dict(size=20, color="#909090"), title_font_size=21)
    fig.update_layout(plot_bgcolor="#000000", paper_bgcolor="#000000")
    fig.update_layout(showlegend=False)

    fig.update_layout(width=width, height=height, title="Corona Brightness Profile @ 3 Solar Diameters - 24 Hours",
                      xaxis_title="Circumferential Coverage<br><sub>http://DunedinAurora.nz</sub>",
                      yaxis_title="Brightness - Arbitrary Units")


    fig.write_image(file=savefile, format='jpg')


def plot(dates, pixel_count, filename, width, height):
    savefile = filename
    # pixel_count = median_filter(pixel_count)
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

    fig.update_xaxes(nticks=12, tickangle=45)

    if max(pixel_count) > cme_min:
        ymax = max(pixel_count) * 1.1
    else:
        ymax = cme_min

    ymin = min(pixel_count)
    fig.update_yaxes(range=[ymin, ymax])

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


def count_greys(array):
    num_pixels = array.sum()
    return num_pixels


def crop_image(image, imagewidth, imageheight, topoffset, bottomoffset):
    cropped_img = image[imageheight - bottomoffset:imageheight - topoffset, 0:imagewidth]
    # print(cropped_img)
    return cropped_img


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


def normalise_image(detrended_img):
    # normlise a numpy array between 0 - 255
    returnarray = []
    im_min = detrended_img.min()
    im_max = detrended_img.max()

    for row in detrended_img:
        for column in row:
            newvalue = (column - im_min) / (im_max - im_min)
            newvalue = int(newvalue * 254)
            returnarray.append(newvalue)
    returnarray = np.reshape(returnarray, (512, 512))
    returnarray = np.array(returnarray, np.uint8)
    # returnarray = np.array(detrended_img, np.uint8)
    return returnarray


def erode_dilate_img(image_to_process):
    # Erode and Dilate the image to clear up noise
    # Erosion will trim away pixels (noise)
    # dilation puffs out edges
    kernel = np.ones((3,3), np.uint8)
    outputimg = cv2.erode(image_to_process, kernel, iterations=2)
    outputimg = cv2.dilate(outputimg, kernel, iterations=1)
    return outputimg


def wrapper(storage_folder, analysis_folder):
    # get a list of the current stored images.
    # IGNORE files with the suffix .no as they are corrupted or reconstructed by the LASCO team, and the
    # interpolated data in inaccurate
    dirlisting = []
    path = os.path.join(storage_folder, "*.jpg")
    for name in glob.glob(path):
        name = os.path.normpath(name)
        seperator = os.path.sep
        n = name.split(seperator)
        nn = n[1]
        dirlisting.append(nn)

    # make sure they are in chronological order by name
    dirlisting.sort()

    # We do not need ALL of the images in the Lasco folder, only the last day or so. Approx
    # 100 images per day.
    truncate = 120
    dirlisting = dirlisting[-truncate:]
    avg_array = []
    cme_count = []
    cme_spread = []
    dates = []

    # Parsing thru the list of images
    for i in range (0, len(dirlisting)):
        p = storage_folder + "//" + dirlisting[i]

        # load and preprocess the image
        img = image_load(p)
        img = erode_dilate_img(img)

        # Occasionally images are loaded that are broken. If this is not the case...
        if img is not None:
            # greyscale the image
            img_g = greyscale_img(img)

            # Create an array of pictures with which to create a running average image
            pic = np.array(img_g, np.float64)
            avg_array.append(pic)

            # create an average of "x" number of images
            if len(avg_array) >= 3:
                # ALWAYS POP
                avg_array.pop(0)
                # the average image
                pic_new = np.mean(avg_array, axis=0)
                pic_new = normalise_image(pic_new)

                #  convolve the returned residuals image from polar to rectangular co-ords. the data is appended to
                #  an array
                radius = 220
                angle = 360
                t = []
                for j in range(radius, 0, -1):
                    for k in range(0, angle):
                        coords = polar_to_rectangular(k, j)
                        pixelvalue = pic_new[coords[1], coords[0]]
                        t.append(pixelvalue)

                # Convert the 1D array into a 2D image.
                # Crop the part that is the detection slot for CMEs near the suns surface
                array = np.reshape(np.array(t), (radius, angle))
                img_cropped = crop_image(array, angle, radius, 40, 50)

                # ====================================================================================
                # determine if there is sufficient change across the cropped image to represent a CME
                # ====================================================================================
                t = dirlisting[i].split("_")
                posixtime = filehour_converter(t[0], t[1])

                hr = posix2utc(posixtime, "%Y-%m-%d %H:%M")
                cme_sum = process_columns(img_cropped)
                # build up an array of the CME column data
                cme_spread.append(cme_sum)
                value = sum(cme_sum)
                cme_count.append(value)

                # cme_spread.append(cme_diffs)
                dates.append(hr)

                # Annotate image for display
                array = annotate_image(array, angle, radius, hr)

                f_image = analysis_folder + "//" + "dt_" + dirlisting[i]
                # image_save(f_image, img_cropped)
                image_save(f_image, array)
                print("dt", i, len(dirlisting))

    # # create video of the last 24 hours from the Analysis folder.
    # # approx no of images in a day
    # imagelist_analysis = os.listdir(analysis_folder)
    # imagelist_analysis.sort()
    # if len(imagelist_analysis) > truncate:
    #     imagelist_analysis = imagelist_analysis[-truncate:]
    # imagelist_analysis.sort()
    # print("creating video...")
    # create_video(imagelist_analysis, analysis_folder, "cme.avi")
    # create_gif(imagelist_analysis, analysis_folder, "cme.gif")

    # create video of the last 24 hours from the enhanced folder.
    # approx no of images in a day is 30 for the enhanced folder!
    imagelist_enhanced = os.listdir("enhanced_512")
    imagelist_enhanced.sort()
    if len(imagelist_enhanced) > 30:
        imagelist_enhanced = imagelist_enhanced[-truncate:]
    imagelist_enhanced.sort()
    print("creating video...")
    # create_video(imagelist_enhanced, "enhanced_512", "whole_disc.avi")
    create_gif(imagelist_enhanced, "enhanced_512", "whole_disc.gif")

    # The data files need to be truncated to the last 100 entries - approx 24 hours
    if len(dates) > truncate:
        dates = dates[-truncate:]
        cme_count = cme_count[-truncate:]
        cme_spread = cme_spread[-truncate:]

    print("creating CME plot files...")
    # Detrend the dme data to flatten out gradual albedo changes
    dt_end = standard_stuff.calc_end(cme_count)
    dt_mid = standard_stuff.calc_middle(cme_count)
    dt_start = standard_stuff.calc_start(cme_count)
    dt_total = dt_start + dt_mid + dt_end
    maxpixels = angle * radius
    detrended = []
    for dt, cme in zip(dt_total, cme_count):
        d = cme - dt
        d = d / maxpixels
        d = round(d, 4)
        detrended.append(d)

    detrended = median_filter(detrended)
    plot(dates, detrended, "cme_dtrend.jpg", 1000, 600)
    plot_diffs(cme_spread, "cme_diffs.jpg", 1700, 600)
    plot_diffs_polar(cme_spread, "cme_polar.jpg", 800, 950)

    # If the max value of the detrended data is over 0.5 then we can write an alert for potential
    # CMEs to check.
    px = max(detrended)
    print(px)
    hr = dates[detrended.index(max(detrended))]
    text_alert(px, hr)

    print("All finished!")
