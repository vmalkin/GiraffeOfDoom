import datetime
import time
import urllib.request
import os
import cv2
import numpy as np
import calendar
from PIL import Image
from math import sin, cos, radians
from statistics import median
from plotly import graph_objects as go

# offset values when coronagraph mask support-vane in top-right position
offset_x = -5
offset_y = 10

image_size = 512
imagecentre = image_size / 2
cme_min = 0.4
cme_partial = 0.6
cme_halo = 0.8


def get_resource_from_url(url_to_get):
    response = ""
    try:
        request = urllib.request.Request(url_to_get, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(request, timeout=10)

    except:
        # logging.error("Unable to load/save image from URL: " + str(imageurl) + " " + str(filename))
        print("unable to load URL", url_to_get)

    return response


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def parse_image_from_url(response, img_latest):
    with open(img_latest, 'wb') as f:
        f.write(response.read())


def parse_text_from_url(response):
    # the response is a list of byte objects.
    returnlist = []
    for line in response:
        s = str(line)
        s = s.split("\\")
        s = s[0]
        s = s.strip()
        s = s[2:27]
        returnlist.append(s)
    return returnlist


def image_load(file_name):
    img = cv2.imread(file_name)
    return img


def image_save(file_name, image_object):
    cv2.imwrite(file_name, image_object)


def greyscale_img(image_to_process):
    # converting an Image to grey scale...
    greyimg = cv2.cvtColor(image_to_process, cv2.COLOR_BGR2GRAY)
    return greyimg


# def erode_dilate_img(image_to_process):
#     # Erode and Dilate the image to clear up noise
#     # Erosion will trim away pixels (noise)
#     # dilation puffs out edges
#     kernel2 = np.ones((4, 4), np.uint8)
#     outputimg = cv2.dilate(image_to_process, kernel2, iterations=1)
#
#     kernel1 = np.ones((6, 6), np.uint8)
#     outputimg = cv2.erode(outputimg, kernel1, iterations=1)
#     return outputimg


def add_stamp(banner_text, image_object, filename):
    tt = time.time()
    tt = posix2utc(tt, "%Y-%m-%d %H:%M")
    cv2. rectangle(image_object, (0, 449), (511, 511), (255, 255, 255), -1)
    cv2.rectangle(image_object, (0, 0), (511, 20), (255, 255, 255), -1)
    colour = (0, 0, 0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 0.5
    font_color = colour
    font_thickness = 1
    banner = banner_text
    x, y = 5, 15
    cv2.putText(image_object, banner, (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)

    banner = 'LASCO coronagraph. Updated ' + tt + " UTC."
    x, y = 5, 466
    cv2.putText(image_object, banner, (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)

    font_size = 0.4
    font_color = colour
    font_thickness = 1

    banner = filename
    x, y = 5, 483
    cv2.putText(image_object, banner, (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)
    banner = 'Courtesy of SOHO/LASCO consortium. SOHO is a project of'
    x, y = 5, 496
    cv2.putText(image_object, banner, (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)
    banner = 'international cooperation between ESA and NASA'
    x, y = 5, 508
    cv2.putText(image_object, banner, (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)


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


def annotate_image(array, width, height, timevalue):
    cimage = cv2.cvtColor(array, cv2.COLOR_GRAY2BGR)
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


def count_nonzero(array):
    # COunt non zero pixels in a zone just above the solar surface.
    try:
        num_pixels = cv2.countNonZero(array)
    except Exception:
        num_pixels = 0
    return num_pixels


def create_mask(image, imagewidth, imageheight, topoffset, bottomoffset):
    mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (0, imageheight - topoffset), (imagewidth, imageheight - bottomoffset), 255, -1)
    return mask


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


def text_alert(px, hr):
    # %Y-%m-%d %H:%M
    timestring = hr
    hr = hr.split(" ")
    hr = hr[0]
    hr = hr.split("-")
    new_hr = hr[0] + "/" + hr[1] + "/" + hr[2]
    url = "https://stereo-ssc.nascom.nasa.gov/browse/" + new_hr +  "/ahead/cor2_rdiff/512/thumbnail.shtml"
    stereo_url = "<a href=\"" + url + "\" target=\"_blank\">" + "Stereo Science Centre</a>"
    savefile = "cme_alert.php"

    if px >= cme_min:
        msg = "A possible CME has been detected with " + str(int(px * 100)) + "% coverage"
        if px >= cme_partial:
            msg = "Warning: A possible PARTIAL HALO CME has been detected with " + str(int(px * 100)) + "% coverage"
            if px >= cme_halo:
                msg = "ALERT: A possible FULL HALO CME has been detected with " + str(int(px * 100)) + "% coverage"
        msg = msg + "<br>Confirm Earth impact with STEREO A satellite data:"

        msg_alert = "<p>" + timestring + "<br>" + msg +  " " + stereo_url
        with open(savefile, "w") as s:
            s.write(msg_alert)


def processimages_detrend(listofimages, storage_folder, analysisfolder):
    avg_array = []
    pixel_count = []
    dates = []
    for i in range(0, len(listofimages)):
        p = storage_folder + "//" + listofimages[i]

        pic = image_load(p)

        pic = greyscale_img(pic)

        # convert image to a single channel
        pic = cv2.split(pic)
        pic = pic[0]

        kernel1 = np.ones((3, 3), np.uint8)
        pic = cv2.erode(pic, kernel1, iterations=1)
        avg_array.append(pic)

        # 100 images is about a day
        if len(avg_array) >= 100:
            # ALWAYS POP
            avg_array.pop(0)
            avg_img = np.mean(avg_array, axis=0)

            pic = np.float32(pic)
            avg_img = np.float32(avg_img)

            detrended_img = cv2.subtract(pic, avg_img)
            ret, detrended_img = cv2.threshold(detrended_img, 3, 255, cv2.THRESH_BINARY)
            final_img = np.uint8(detrended_img)

            # convert the image from polar to rectangular coords in order to more easily
            # map CME occurences and identify halo CMEs
            dst = 220
            ang = 360
            t = []
            for dist in range(dst, 0, -1):
                for angle in range(0, ang):
                    coords = polar_to_rectangular(angle, dist)
                    t.append(final_img[coords[1], coords[0]])

            # https://www.geeksforgeeks.org/convert-a-numpy-array-to-an-image/
            # array = np.array(t)
            array = np.reshape(np.array(t), (dst, ang))

            mask = create_mask(array, ang, dst, 40, 50)
            masked = cv2.bitwise_and(array, mask)

            # Pixelcounter to create graphic pf CMEs
            # A full halo CME should produce counts in the order of 3600
            px = count_nonzero(masked)
            #  pixelcount as a percentage of the area monitored
            px = float(px) / 3600
            px = round(px, 3)
            t = listofimages[i].split("_")
            posixtime = filehour_converter(t[0], t[1])
            hr = posix2utc(posixtime, "%Y-%m-%d %H:%M")

            # Create a text alert to be exported to DunedinAurora and potentially
            # twitter
            text_alert(px, hr)


            pixel_count.append(px)
            dates.append(hr)

            array = annotate_image(array, ang, dst, hr)

            # cv2.imshow('Example - Show image in window', array)
            # cv2.waitKey(0)  # waits until a key is pressed
            # cv2.destroyAllWindows()  # destroys the window showing image

            f_image = analysisfolder + "//" + "dt_" + listofimages[i]
            # add_stamp("High Contrast CME Detection", final_img, f_image)
            image_save(f_image, array)

            print("dt", i, len(listofimages))

    print(len(dates), len(pixel_count))
    pixel_count = median_filter(pixel_count)
    dates.pop(len(dates) - 1)
    dates.pop(0)
    plot(dates, pixel_count, "cme_plot.jpg", 1800, 600)

    dates = dates[-100:]
    pixel_count = pixel_count[-100:]
    plot_mini(dates, pixel_count)


def processimages_display(listofimages, storage_folder, images_folder):
    t = listofimages[0].split("_")
    hourcount = filehour_converter(t[0], t[1])
    hourimage = listofimages[0]

    for i in range(0, len(listofimages)):
        # split the name
        test = listofimages[i].split("_")
        test_hourcount = filehour_converter(test[0], test[1])
        testimage = listofimages[i]
        if test_hourcount - hourcount > (45*60):
            i1 = storage_folder + "/" + hourimage
            img_1 = image_load(i1)

            i2 = storage_folder + "/" + testimage
            img_2 = image_load(i2)

            img_og = greyscale_img(img_1)
            img_ng = greyscale_img(img_2)

            # convert image to a single channel
            img_ng = cv2.split(img_ng)
            img_og = cv2.split(img_og)
            img_ng = img_ng[0]
            img_og = img_og[0]

            # img_og = erode_dilate_img(img_og)
            # img_ng = erode_dilate_img(img_ng)

            # improved histogram function
            clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8, 8))
            img_og = clahe.apply(img_og)
            img_ng = clahe.apply(img_ng)

            # unary operator to invert the image
            img_ng = ~img_ng

            # combine the images to highlight differences
            alpha = 1
            gamma = 0
            new_image = img_ng.copy()
            cv2.addWeighted(img_ng, alpha, img_og, 1 - alpha, gamma, new_image)

            # Adjust contrast and brightness
            d = new_image.copy()
            alpha = 1.2
            beta = -50
            # alpha = 1.2
            # beta = -30
            new_image = cv2.convertScaleAbs(d, alpha=alpha, beta=beta)

            new_image = cv2.applyColorMap(new_image, cv2.COLORMAP_BONE)

            # Save the difference image into the images folder
            add_stamp("Processed at Dunedin Aurora", new_image, hourimage)
            fname = images_folder + "/" + listofimages[i]
            image_save(fname, new_image)
            # print("Display image created..." + fname)

            # LASTLY.....
            hourcount = test_hourcount
            hourimage = testimage


def parseimages(listofimages, imagestore):
    set_downloads = set(listofimages)
    stored = os.listdir(imagestore)
    set_stored = set(stored)
    newfiles = set_downloads.difference(set_stored)
    return newfiles


def downloadimages(listofimages, storagelocation):
    for img in listofimages:
        file = storagelocation + "/" + img
        img1url = baseURL + img
        if os.path.exists(file) is False:
            response1 = get_resource_from_url(img1url)
            print("Saving file ", file)
            parse_image_from_url(response1, file)


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


if __name__ == "__main__":
    computation_start = time.time()
    images_folder = "images_512"
    storage_folder = "lasco_store_512"
    analysis_folder = "analysis_512"

    if os.path.exists(images_folder) is False:
        os.makedirs(images_folder)
    if os.path.exists(storage_folder) is False:
        os.makedirs(storage_folder)
    if os.path.exists(analysis_folder) is False:
        os.makedirs(analysis_folder)

    if os.path.exists("cme_alert.php"):
        os.remove("cme_alert.php")

    tm = int(time.time())
    ymd_now = posix2utc(tm, "%Y%m%d")
    ymd_old = posix2utc((tm - 86400), "%Y%m%d")
    year = posix2utc(tm, "%Y")

    # LASCO coronagraph
    print("Getting images for current epoch")
    baseURL = "https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/" + year + "/c3/" + ymd_now + "/"
    onlinelist = baseURL + ".full_512.lst"
    listofimages = get_resource_from_url(onlinelist)
    listofimages = parse_text_from_url(listofimages)
    newimages = parseimages(listofimages, storage_folder)

    if len(newimages) > 0:
        # rings the terminal bell
        print("\a")
        downloadimages(newimages, storage_folder)

    # Parse for old epoch files that have been added
    print("Getting images for old epoch")
    # ymd_old = "20210807"
    baseURL = "https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/" + year + "/c3/" + ymd_old + "/"
    onlinelist = baseURL + ".full_512.lst"
    listofimages = get_resource_from_url(onlinelist)
    listofimages = parse_text_from_url(listofimages)

    newimages = parseimages(listofimages, storage_folder)
    # print("New images: ", newimages)

    if len(newimages) > 0:
        # rings the terminal bell
        print("\a")
        downloadimages(newimages, storage_folder)

    # get a list of the current stored images.
    dirlisting = os.listdir(storage_folder)

    # make sure they are in chronological order
    dirlisting.sort()

    # process the stored images so far to get latest diffs
    print("Preparing enhanced images for display...")
    processimages_display(dirlisting, storage_folder, images_folder)

    print("Preparing enhanced images for analysis...")
    processimages_detrend(dirlisting, storage_folder, analysis_folder)

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

    computation_end = time.time()
    elapsed_mins = round((computation_end - computation_start) / 60, 1)
    print("Elapsed time: ", elapsed_mins)
    print("Finished processing.")
