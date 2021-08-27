import datetime
import time
import urllib.request
import os
import mgr_analyser

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
            with open(file, 'wb') as f:
                f.write(response1.read())


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

    if len(newimages) > 0:
        # rings the terminal bell
        print("\a")
        downloadimages(newimages, storage_folder)

    try:
        mgr_analyser.wrapper()
    except:
        pass

    computation_end = time.time()
    elapsed_mins = round((computation_end - computation_start) / 60, 1)
    print("Elapsed time: ", elapsed_mins)
    print("Finished processing.")
