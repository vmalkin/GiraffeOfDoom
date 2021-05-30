import datetime
import time
import urllib.request
import pickle
import os
import cv2
import numpy as np
import calendar
import plotly.graph_objects as go


def get_resource_from_url(url_to_get):
    response = ""
    try:
        request = urllib.request.Request(url_to_get, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(request, timeout=10)

    except urllib.request.HTTPError:
        # logging.error("Unable to load/save image from URL: " + str(imageurl) + " " + str(filename))
        print("unable to load URL")
        print(url_to_get)

    # finally:
    #     print("Unable to get any further data from URL: ", url_to_get)

    return response


def load_values(pickle_file):
    returnvalue = variables
    if os.path.exists(pickle_file) is True:
        try:
            returnvalue = pickle.load(open(pickle_file, "rb"))
        except EOFError:
            print("Pickle file is empty")
    return returnvalue


def save_values(save_value, pickle_file):
    pickle.dump(save_value, open(pickle_file, "wb"), 0)


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def parse_image_fromURL(response, img_latest):
    with open(img_latest, 'wb') as f:
        f.write(response.read())


def parse_text_fromURL(response):
    # the response is a list of byte objects.
    returnlist = []
    for line in response:
        s = str(line)
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


def erode_dilate_img(image_to_process):
    # Erode and Dilate the image to clear up noise
    # Erosion will trim away pixels (noise)
    # dilation puffs out edges
    kernel1 = np.ones((5, 5), np.uint8)
    outputimg = cv2.erode(image_to_process, kernel1, iterations=1)
    kernel2 = np.ones((5, 5), np.uint8)
    outputimg = cv2.dilate(outputimg, kernel2, iterations=1)
    return outputimg


def add_stamp(image_object, filename):
    cv2. rectangle(image_object, (0, 900), (1024,1024), (255,255,255), -1 )
    colour = (0, 0, 0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 1.0
    font_color = colour
    font_thickness = 2
    banner = 'DunedinAurora.NZ - CME Detection.'
    x, y = 10, 925
    cv2.putText(image_object, banner, (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)

    font_size = 0.7
    font_color = colour
    font_thickness = 1
    banner = filename
    x, y = 10, 950
    cv2.putText(image_object, banner, (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)
    banner = 'Courtesy of SOHO/LASCO consortium. SOHO is a project of'
    x, y = 10, 975
    cv2.putText(image_object, banner, (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)
    banner = 'international cooperation between ESA and NASA'
    x, y = 10, 1000
    cv2.putText(image_object, banner, (x, y), font, font_size, font_color, font_thickness, cv2.LINE_AA)


def filehour_converter(yyyymmdd, hhmm):
    year = (yyyymmdd[:4])
    month = (yyyymmdd[4:6])
    day = (yyyymmdd[6:])
    hour = (hhmm[:2])
    min = (hhmm[2:])
    utc_string = year + '-' + month + '-' + day  + ' ' + hour  + ':' +  min
    dt = datetime.datetime.strptime(utc_string, '%Y-%m-%d %H:%M')
    ts = calendar.timegm(dt.timetuple())
    return ts


def countpixels(image):
    # create a mask to be added o
    n = image.copy()
    s = image.copy()
    south = cv2.rectangle(s, (0,0), (1023, 512), (255,255,255),-1)
    north = cv2.rectangle(n, (0, 512), (1023, 1023), (255,255,255),-1)
    count_n = (1024*1024) - cv2.countNonZero(north)
    count_s = (1024*1024) - cv2.countNonZero(south)
    return [count_n, count_s]


def countpixels_total(outputtotal):
    count_t = (1024 * 1024) - cv2.countNonZero(outputtotal)
    return count_t


def processimages_analysis(listofimages, storage_folder, analysisfolder):
    t = listofimages[0].split("_")
    hourcount = filehour_converter(t[0], t[1])
    hourimage = listofimages[0]
    mask = create_polar_mask(hourimage)
    pixelcount = []
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

            img_og = erode_dilate_img(img_og)
            img_ng = erode_dilate_img(img_ng)
            img_to = img_og
            img_tn = img_ng

            # add mask.
            img_ng = cv2.bitwise_and(img_ng, mask, mask=mask)
            img_og = cv2.bitwise_and(img_og, mask, mask=mask)

            # improved histogram function
            clahe = cv2.createCLAHE(clipLimit=5, tileGridSize=(8,8))
            img_og = clahe.apply(img_og)
            img_ng = clahe.apply(img_ng)
            img_to = clahe.apply(img_to)
            img_tn = clahe.apply(img_tn)

            # unary operator to invert the image
            img_ng = ~img_ng
            img_tn = ~img_tn

            # combine the images to highlight differences
            alpha = 1.2
            gamma = 0
            new_image = img_ng.copy()
            new_total = img_tn.copy()
            cv2.addWeighted(img_ng, alpha, img_og, 1 - alpha, gamma, new_image)
            cv2.addWeighted(img_tn, alpha, img_to, 1 - alpha, gamma, new_total)

            # Adjust contrast and brightness
            d = new_image.copy()
            alpha = 1.2
            beta = -50
            new_image = cv2.convertScaleAbs(d, alpha=alpha, beta=beta)
            ret, outputimg = cv2.threshold(new_image, 130, 255, cv2.THRESH_BINARY)
            ret1, outputtotal = cv2.threshold(new_total, 130, 255, cv2.THRESH_BINARY)

            # here we need to count pixels found in the north and south parts of the image to
            # determine if a CME halo is present
            count = countpixels(outputimg)
            count_total = countpixels_total(outputtotal)
            dp = posix2utc(test_hourcount, '%Y-%m-%d %H:%M') + "," + str(count[0]) + "," + str(count[1]) + "," + str(count_total)
            # dp = [posix2utc(test_hourcount, '%Y-%m-%d %H:%M'),count[0], count[1]]
            pixelcount.append(dp)

            # Save the difference image into the images folder
            add_stamp(outputimg, hourimage)
            fname = analysisfolder + "/" + listofimages[i]
            image_save(fname, outputimg)
            print("Polar CME image created..." + fname)

            # LASTLY.....
            hourcount = test_hourcount
            hourimage = testimage
    return pixelcount

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
            clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8,8))
            img_og = clahe.apply(img_og)
            img_ng = clahe.apply(img_ng)

            # unary operator to invert the image
            img_ng = ~img_ng

            # combine the images to highlight differences
            alpha = 1.2
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
            add_stamp(new_image, hourimage)
            fname = images_folder + "/" + listofimages[i]
            image_save(fname, new_image)
            print("Display image created..." + fname)

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
            parse_image_fromURL(response1, file)


def create_polar_mask(image):
    print(image)
    img = np.zeros((1024, 1024), np.uint8)
    colour = (255, 255, 255)

    # occulating disk
    cv2.circle(img, (515, 500), 83, colour, -1)

    # top zone
    triangle = [(0, 0), (0, 1023), (512,512)]
    cv2.fillPoly(img, np.array([triangle]), colour)

    # bottom zone
    triangle = [(512,512), (1023, 100), (1023,1023)]
    cv2.fillPoly(img, np.array([triangle]), colour)

    img = ~img
    return img


# def cme_detect_farneback(done_images, imagesfolder):
#     if len(done_images) > 1:
#         # filename = imagesfolder + "/" + done_images[0]
#         filename = done_images[0]
#         img = image_load(filename)
#         hsv = np.zeros_like(img)
#         hsv[..., 1] = 255
#
#         for i in range(1, len(done_images) - 1):
#             # file_old = imagesfolder + "/" + done_images[i - 1]
#             file_old = done_images[i - 1]
#             img_old = image_load(file_old)
#
#             # file_new = imagesfolder + "/" + done_images[i]
#             file_new = done_images[i]
#             img_new = image_load(file_new)
#
#             # convert image to a single channel
#             img_new = cv2.split(img_new)
#             img_old = cv2.split(img_old)
#             img_new = img_new[0]
#             img_old = img_old[0]
#
#             flow = cv2.calcOpticalFlowFarneback(img_old, img_new, None, 0.5, 3, 15, 3, 7, 1.5, 0)
#             mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
#             hsv[..., 0] = ang * 180 / np.pi / 2
#             hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
#             bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
#
#             # new_image = cv2.applyColorMap(bgr, cv2.COLORMAP_HSV)
#             nom = done_images[i].split("\\")
#             nom = nom[1].split("_")
#             f = "cme_" + nom[0] + "_" + nom[1] + ".jpg"
#             fname = imagesfolder + "/" + f
#             image_save(fname, bgr)
#             print("Optical flow image created: ", fname)
#
#
# def cme_detection_lucask(done_images, imagesfolder):
#     if len(done_images) > 1:
#         filename = imagesfolder + "/" + done_images[0]
#         img = image_load(filename)
#         hsv = np.zeros_like(img)
#         hsv[..., 1] = 255


def plot_chart(pixels):
    xlabels = []
    north = []
    south = []
    total = []

    for item in pixels:
        i = item.split(",")
        xlabels.append(i[0])
        north.append(int(i[1]))
        south.append(int(i[2]))
        total.append(int(i[3]))

    fig = go.Figure()
    fig.add_trace((go.Scatter(x=xlabels, y=total, mode="lines", name="Total CMEs",
                              line=dict(width=3, color="#008000"))))
    fig.add_trace((go.Scatter(x=xlabels, y=north, mode="lines", name="North CMEs",
                              line=dict(width=3, color="#800000"))))
    fig.add_trace((go.Scatter(x=xlabels, y=south, mode="lines", name="South CMEs",
                              line=dict(width=3, color="#000080"))))

    fig.update_layout(plot_bgcolor="#a0a0a0", paper_bgcolor="#a0a0a0")
    fig.update_layout(width=1000, height=600, title="CME Detection",
                      xaxis_title="Date/time UTC", yaxis_title="pixel count")
    fig.write_image(file="cme.svg", format='svg')


if __name__ == "__main__":
    images_folder = "images"
    storage_folder = "lasco_store"
    analysis_folder = "analysis"
    saved_variables = "variables.pkl"
    variables = None

    if os.path.exists(images_folder) is False:
        os.makedirs(images_folder)
    if os.path.exists(storage_folder) is False:
        os.makedirs(storage_folder)
    if os.path.exists(analysis_folder) is False:
        os.makedirs(analysis_folder)

    tm = int(time.time())
    ymd = posix2utc(tm, "%Y%m%d")
    year = posix2utc(tm, "%Y")

    print("Current epoch")
    baseURL = "https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/" + year + "/c3/" + ymd + "/"
    onlinelist = baseURL + ".full_1024.lst"
    print(onlinelist)
    listofimages = get_resource_from_url(onlinelist)
    listofimages = parse_text_fromURL(listofimages)

    newimages = parseimages(listofimages, storage_folder)
    print("New images: ", newimages)

    if len(newimages) > 0:
        # rings the terminal bell
        print("\a")
        downloadimages(newimages, storage_folder)

    print(newimages)
    print(variables)

    # Parse for old epoch files that have been added
    print("Old epoch")
    # ymd = variables["epoch"]
    ymd = str(int(ymd) - 1)
    # ymd = "20210523"
    baseURL = "https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/" + year + "/c3/" + ymd + "/"
    onlinelist = baseURL + ".full_1024.lst"
    print(onlinelist)
    listofimages = get_resource_from_url(onlinelist)
    listofimages = parse_text_fromURL(listofimages)

    newimages = parseimages(listofimages, storage_folder)
    print("New images: ", newimages)

    if len(newimages) > 0:
        # rings the terminal bell
        print("\a")
        downloadimages(newimages, storage_folder)

    print(newimages)
    print(variables)

    # get a list of the current stored images.
    dirlisting = os.listdir(storage_folder)
    # make sure they are in chronological order
    dirlisting.sort()
    print(dirlisting)
    # process the stored images so far to get latest diffs
    processimages_display(dirlisting, storage_folder, images_folder)
    pixels = processimages_analysis(dirlisting, storage_folder, analysis_folder)
    plot_chart(pixels)

    with open("pixelcount.csv", "w") as f:
        f.write("UTC time, North, South, Total\n")
        for line in pixels:
            f.write(line + "\n")
        f.close()

    print("Finished processing.")
