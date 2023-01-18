import os
from PIL import Image
import time
import datetime
import calendar
import glob

stereo = "stereoscopic"
if os.path.exists(stereo) is False:
    os.makedirs(stereo)


def shorten_dirlisting(directory_listing):
    # Return files for the last x hours, as needed.
    cutoff = time.time() - (86400 * 2)  # the last 2 days
    returnarray = []
    for item in directory_listing:
        dt = filename_converter(item, "posix")
        if dt > cutoff:
            returnarray.append(item)
    return returnarray


def filename_converter(filename, switch="posix"):
    # Name has format 20221230_2342_c3_512.jpg
    f = filename.split("_")
    yyyymmdd = f[0]
    hhmm = f[1]
    year = (yyyymmdd[:4])
    month = (yyyymmdd[4:6])
    day = (yyyymmdd[6:])
    hour = (hhmm[:2])
    min = (hhmm[2:])
    utc_string = year + '-' + month + '-' + day + ' ' + hour + ':' + min
    filename = year + '-' + month + '-' + day + '-' + hour + '-' + min + ".jpg"
    # utc time string
    dt = datetime.datetime.strptime(utc_string, '%Y-%m-%d %H:%M')

    if switch == "utc":
        # utc time string
        returnstring = datetime.datetime.strptime(utc_string, '%Y-%m-%d %H:%M')
    elif switch == "filename":
        returnstring = filename
    else:
        returnstring = calendar.timegm(dt.timetuple())
    # return posix by default
    return returnstring


def get_dirlisting(folder):
    dirlisting = []
    path = os.path.join(folder, "*.jpg")
    for name in glob.glob(path):
        name = os.path.normpath(name)
        seperator = os.path.sep
        n = name.split(seperator)
        nn = n[1]
        dirlisting.append(nn)
        # make sure they are in chronological order by name
    dirlisting.sort()
    return dirlisting


def wrapper(directory):
    # create video of the last 24 hours from the enhanced folder.
    # approx no of images in a day is 30 for the enhanced folder!
    stereoarray = []
    dirlisting = get_dirlisting(directory)
    dirlisting = shorten_dirlisting(dirlisting)


    filepath = directory + "/" + dirlisting[0]
    img1 = Image.open(filepath)
    for i in range(1, len(dirlisting)):
        sf = dirlisting[i].split(".")
        stereo_filename = sf[0]
        filepath = directory + "/" + dirlisting[i]
        img2 = Image.open(filepath)
        w = img2.width
        h = img2.height
        stereoimage = Image.new("RGB", [w*2, h])
        stereoimage.paste(img1)
        stereoimage.paste(img2, (img2.size[0], 0))
        stereoarray.append(stereoimage)
        savefile = stereo + "/" + stereo_filename + ".jpg"
        stereoimage.save(savefile)
        img1 = img2

    stereoarray[0].save("stereo_cme.gif",
                      format="GIF",
                      save_all=True,
                      append_images=stereoarray[1:],
                      duration=75,
                      loop=0)
