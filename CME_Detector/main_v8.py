import datetime
import time
import urllib.request
import requests
import os
import mgr_analyser
import mgr_enhancer


def get_resource_from_url(url_to_get):
    response = ""
    try:
        response = requests.get(url_to_get)
        # request = urllib.request.Request(url_to_get, headers={'User-Agent': 'Mozilla/5.0'})
        # response = urllib.request.urlopen(request, timeout=10)

    except:
        # logging.error("Unable to load/save image from URL: " + str(imageurl) + " " + str(filename))
        print("unable to load URL", url_to_get)
        print("Try: pip install --upgrade certifi")

    return response


def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


def parse_text_from_url(response):
    # the response is a list of byte objects.
    response = response.text
    response = response.split("\n")
    returnlist = []
    for item in response:
        returnlist.append(item)
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
                # f.write(response1.read())
                f.write(response1.content)
            f.close()


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
    ymd_old = "20210929"
    baseURL = "https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/" + year + "/c3/" + ymd_old + "/"
    onlinelist = baseURL + ".full_512.lst"
    listofimages = get_resource_from_url(onlinelist)
    listofimages = parse_text_from_url(listofimages)

    newimages = parseimages(listofimages, storage_folder)


    if len(newimages) > 0:
        # rings the terminal bell
        print("\a")
        downloadimages(newimages, storage_folder)


    # Analyse and enhance stored images
    try:
        mgr_analyser.wrapper(storage_folder, analysis_folder)
    except:
        print("The Analyser has failed!")

    # try:
    mgr_enhancer.wrapper(storage_folder, images_folder)
    # except:
    #     print("The Enhancer has failed!")

    computation_end = time.time()
    elapsed_mins = round((computation_end - computation_start) / 60, 1)
    print("Elapsed time: ", elapsed_mins)
    print("Finished processing.")
