import datetime
import time
import re
import requests
import os

suvi_store = "suvi_store"
diffs_store = "difference_images"
# file path seperator / or \ ???
pathsep = os.sep
suvi_url = "https://services.swpc.noaa.gov/images/animations/suvi/primary/171/"


def get_resource_from_url(url_to_get):
    response = ""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url_to_get, headers=headers)
    except:
        print("unable to load URL", url_to_get)
        print("Try: pip install --upgrade certifi")
    return response


# def posix2utc(posixtime, timeformat):
#     # '%Y-%m-%d %H:%M'
#     utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
#     return utctime


def parseimages(listofimages, imagestore):
    set_downloads = set(listofimages)
    stored = os.listdir(imagestore)
    set_stored = set(stored)
    newfiles = set_downloads.difference(set_stored)
    return newfiles


def downloadimages(listofimages, storagelocation):
    for img in listofimages:
        file = storagelocation + "/" + img
        i = img.split(".")
        baddy = str(i[0])
        badfile = storagelocation + "/" + baddy + ".no"
        img1url = baseURL + img
        if os.path.exists(badfile) is False:
            if os.path.exists(file) is False:
                response1 = get_resource_from_url(img1url)
                print("Saving file ", file)
                with open(file, 'wb') as f:
                    # f.write(response1.read())
                    f.write(response1.content)
                f.close()
        else:
            print("Corrupted image bypassed from processing")


def get_imagelist(url_to_get):
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url_to_get, headers=headers)
    r = r.text.split("\n")
    #  The response is now delimited on newlines. We can get rid lines to only have the HTML with the images
    # Remove the content above and below the table that contains images

    r = r[13:]
    r = r[:-4]

    # Now split the lines around image file names. Return only the ones 512 in size
    returnlist = []
    for line in r:
        l1 = line.split("href=\"")
        if len(l1) == 2:
            l2 = (l1[1])
            l2 = l2.split("\"")
            filename = l2[0]
            # if re.search("c3_1024", filename):
            if re.search("c3_512", filename):
                returnlist.append(filename)

    return returnlist

def download_suvi(lasco_url, storage_folder):
    print(lasco_url)
    listofimages = get_imagelist(lasco_url)
    newimages = parseimages(listofimages, storage_folder)
    if len(newimages) > 0:
        # rings the terminal bell
        print("\a")
        downloadimages(newimages, storage_folder)


if __name__ == "__main__":
    if os.path.exists(suvi_store) is False:
        os.makedirs(suvi_store)
    if os.path.exists(diffs_store) is False:
        os.makedirs(diffs_store)

    download_suvi(suvi_url, suvi_store)




