import datetime
import time
import urllib.request
import pickle
import os
import cv2
import numpy as np
import calendar
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statistics import median
from PIL import Image, ImageDraw

def get_resource_from_url(url_to_get):
    response = ""
    try:
        request = urllib.request.Request(url_to_get, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(request, timeout=10)

    except urllib.request.HTTPError:
        # logging.error("Unable to load/save image from URL: " + str(imageurl) + " " + str(filename))
        print("unable to load URL", url_to_get)

    return response


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


def erode_dilate_img(image_to_process):
    # Erode and Dilate the image to clear up noise
    # Erosion will trim away pixels (noise)
    # dilation puffs out edges
    kernel2 = np.ones((4, 4), np.uint8)
    outputimg = cv2.dilate(image_to_process, kernel2, iterations=1)

    kernel1 = np.ones((6, 6), np.uint8)
    outputimg = cv2.erode(outputimg, kernel1, iterations=1)
    return outputimg


def add_stamp(image_object, filename):
    tt = time.time()
    tt = posix2utc(tt, "%Y-%m-%d %H:%M")
    cv2. rectangle(image_object, (0, 449), (511,511), (255,255,255), -1 )
    cv2.rectangle(image_object, (0, 0), (511, 20), (255, 255, 255), -1)
    colour = (0, 0, 0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 0.5
    font_color = colour
    font_thickness = 1
    banner = 'Processed by http://DunedinAurora.NZ'
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
    utc_string = year + '-' + month + '-' + day  + ' ' + hour  + ':' +  min
    dt = datetime.datetime.strptime(utc_string, '%Y-%m-%d %H:%M')
    ts = calendar.timegm(dt.timetuple())
    return ts


def processimages_detrend(listofimages, storage_folder, analysisfolder):
    avg_array = []
    pixel_count = []
    mask = create_polar_mask(512, 5, -10)

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
            avg_img = np.mean(avg_array, axis=0)

            pic = np.float32(pic)
            avg_img = np.float32(avg_img)

            detrended_img = cv2.subtract(pic, avg_img)
            ret,detrended_img = cv2.threshold(detrended_img, 6, 255, cv2.THRESH_BINARY)
            detrended_img = np.float32(detrended_img)

            # detrended_img = np.uint8(detrended_img)
            # avg_img = np.uint8(avg_img)
            # detrended_img = cv2.adaptiveThreshold(avg_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 0)

            # # [blend_images]
            # alpha = 0.5
            # beta = (1.0 - alpha)
            # detrended_img = cv2.addWeighted(pic, alpha, avg_img, beta, 0.0)

            # detrended_img = pic - avg_img
            # detrended_img = detrended_img * 4

            # # normalise the image
            # detrended_img = detrended_img - detrended_img.min()
            # detrended_img = (detrended_img / detrended_img.max()) * 255

            savefile = analysisfolder + "//" + "dt_" + listofimages[i]
            add_stamp(detrended_img, savefile)

            image_save(savefile, detrended_img)

            px = cv2.countNonZero(detrended_img)
            pixel_count.append(px)

            print("dt", i, len(listofimages))
            avg_array.pop(0)

    with open("pixelcount.csv", "w") as p:
        for line in pixel_count:
            p.write(str(line) + "\n")
        p.close()


def processimages_opticalflow(listofimages, storage_folder, images_folder):
    pr = storage_folder + "//" + listofimages[0]
    prev = image_load(pr)
    hsv = np.zeros_like(prev)
    hsv[..., 1] = 255

    for i in range(1, len(listofimages)):
        nx = storage_folder + "//" + listofimages[i]
        next = image_load(nx)

        # convert image to a single channel
        prev = cv2.split(prev)
        next = cv2.split(next)
        prev = prev[0]
        next = next[0]

        flow = cv2.calcOpticalFlowFarneback(prev, next, None, 0.5, 3, 15, 3, 5, 2, 0)
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        savefile = images_folder + "//" + "fl_" + listofimages[i]
        cv2.imwrite(savefile, bgr)
        print("fl", i, len(listofimages))
        prev = next


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
            add_stamp(new_image, hourimage)
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
            parse_image_fromURL(response1, file)


def create_polar_mask(masksize, xoffset, yoffset):
    dist_full = masksize - 1
    dist_half = int(masksize / 2)
    dist_quarter = int(masksize / 4)

    img = np.zeros((masksize, masksize), np.uint8)
    colour = (255, 255, 255)

    # occulating disk
    cv2.circle(img, (dist_half + xoffset, dist_half + yoffset), 53, colour, -1)

    # # top zone
    # triangle = [(0, 10), (0, dist_full-10), (dist_half,dist_half)]
    # cv2.fillPoly(img, np.array([triangle]), colour)

    # # bottom zone
    # triangle = [(dist_half,dist_half), (dist_full, 0), (dist_full,dist_full)]
    # cv2.fillPoly(img, np.array([triangle]), colour)

    # # Blank the top and bottom zones so they dont go all the way to the edge
    # cv2.rectangle(img, (0, 0), (dist_full, dist_quarter), (255, 255, 255), -1)
    # cv2.rectangle(img, (0, dist_full-dist_quarter), (dist_full, dist_full), (255, 255, 255), -1)

    # img = ~img
    # cv2.imshow("Display window", img)
    # k = cv2.waitKey(0)
    return img


def calc_median(array):
    temp = []
    half_len = 4
    u = 0
    if len(array) > half_len * 2:
        for i in range(half_len, len(array) - half_len):
            t = []
            for j in range(0, half_len):
                t.append(array[i + j])
            u = median(t)
            temp.append(u)
    return temp


def recursive_smooth(array, parameter):
    temp = []
    st_prev = array[0]
    for i in range(1, len(array)):
        st_now = (parameter * array[i]) + ((1 - parameter) * st_prev)
        temp.append(st_now)
        st_prev = st_now
    return temp


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
    images_folder = "images_512"
    storage_folder = "lasco_store_512"
    analysis_folder = "analysis_512"

    if os.path.exists(images_folder) is False:
        os.makedirs(images_folder)
    if os.path.exists(storage_folder) is False:
        os.makedirs(storage_folder)
    if os.path.exists(analysis_folder) is False:
        os.makedirs(analysis_folder)

    tm = int(time.time())
    ymd_now = posix2utc(tm, "%Y%m%d")
    ymd_old = posix2utc((tm - 86400), "%Y%m%d")
    year = posix2utc(tm, "%Y")

    # LASCO coronagraph
    print("Getting images for current epoch")
    baseURL = "https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/" + year + "/c3/" + ymd_now + "/"
    onlinelist = baseURL + ".full_512.lst"
    listofimages = get_resource_from_url(onlinelist)
    listofimages = parse_text_fromURL(listofimages)
    newimages = parseimages(listofimages, storage_folder)

    if len(newimages) > 0:
        # rings the terminal bell
        print("\a")
        downloadimages(newimages, storage_folder)

    # Parse for old epoch files that have been added
    print("Getting images for old epoch")
    # ymd_old = "20210716"
    baseURL = "https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/" + year + "/c3/" + ymd_old + "/"
    onlinelist = baseURL + ".full_512.lst"
    listofimages = get_resource_from_url(onlinelist)
    listofimages = parse_text_fromURL(listofimages)

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

    # dirlisting = os.listdir(analysis_folder)
    # print("Preparing images for optical flow...")
    # processimages_opticalflow(dirlisting, analysis_folder, analysis_folder)

    # create an animated GIF of the last 24 images from the Analysis folder.
    imagelist = os.listdir(analysis_folder)
    imagelist.sort()
    if len(imagelist) > 24:
        cut = len(imagelist) - 24
        imagelist = imagelist[cut:]
    imagelist.sort()
    print("creating animated GIF...")
    create_gif(imagelist, images_folder)

    print("Finished processing.")
