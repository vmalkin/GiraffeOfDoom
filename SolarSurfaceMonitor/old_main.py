#  fix opencv error in windows with:
#  https://stackoverflow.com/questions/63869389/error-could-not-build-wheels-for-opencv-python-which-use-pep-517-and-cannot-b
# Suvi imgaes from:
#

import cv2
import numpy as np
import requests
import os
import glob


suvi_store = "suvi_store"
diffs_store = "difference_images"
# file path seperator / or \ ???
pathsep = os.sep
suvi_url = "https://services.swpc.noaa.gov/images/animations/suvi/primary/171/"

def directory_checkcreate():
    # Checks if required directories exist, if no, creates them
    if os.path.exists(suvi_store) is False:
        os.makedirs(suvi_store)

    if os.path.exists(diffs_store) is False:
        os.makedirs(diffs_store)

def local_file_list_build(directory):
    # Builds and returns a list of files contained in the directory.
    # List is sorted into A --> Z order
    dirlisting = []
    path = directory + pathsep + "*.*"
    for name in glob.glob(path):
        name = os.path.normpath(name)
        seperator = os.path.sep
        n = name.split(seperator)
        nn = n[1]
        dirlisting.append(nn)
    dirlisting.sort()
    return dirlisting

def url_get_resource(url_to_get):
    response = ""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url_to_get, headers=headers)
    except:
        print("unable to load URL", url_to_get)
        print("Try: pip install --upgrade certifi")
    return response


def get_imagelist(url_to_get):
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url_to_get, headers=headers)
    r = r.text.split("\n")
    #  The response is now delimited on newlines. We can get rid lines to only have the HTML with the images
    # Remove the content above and below the table that contains images

    r = r[9:]
    r = r[:-3]

    # Now split the lines around image file names. Return only the ones 512 in size
    returnlist = []
    for line in r:
        l = line.split("href=")
        l1 = l[1].split(">or_suvi")
        f = l1[0][1:-1]
        returnlist.append(f)
    return returnlist


def downloadimages(listofimages, storagelocation):
    for img in listofimages:
        file = storagelocation + pathsep + img
        img1url = suvi_url + img
        response1 = url_get_resource(img1url)
        print("Saving file ", file)
        with open(file, 'wb') as f:
            # f.write(response1.read())
            f.write(response1.content)
        f.close()


if __name__ == '__main__':
    directory_checkcreate()

    onlinefiles = get_imagelist(suvi_url)
    downloadimages(onlinefiles, suvi_store)


    # for i in range(1, len(files)):
    #     old_name = suvi_store + pathsep + files[i - 1]
    #     new_name = suvi_store + pathsep +  files[i]
    #
    #
    #
    #     img_old = cv2.imread(old_name, cv2.IMREAD_GRAYSCALE)
    #     img_new = cv2.imread(new_name, cv2.IMREAD_GRAYSCALE)
    #
    #     img_diff = img_new - img_old
    #
    #     diff_filename = diffs_store + pathsep +  str(i) + "_df.jpg"
    #     cv2.imwrite(diff_filename, img_diff)




    # img1 = cv.imread("or_suvi-l2-ci171_g18_s20230525T224000Z_e20230525T224400Z_v1-0-1.png", cv.IMREAD_GRAYSCALE)
    # img2 = cv.imread("or_suvi-l2-ci171_g18_s20230525T224400Z_e20230525T224800Z_v1-0-1.png", cv.IMREAD_GRAYSCALE)
    #
    # imgd = img2 - img1
    # cv.imwrite("diff.jpg", imgd)
    # # cv.imshow('unchanged image', imgd)
    # # cv.waitKey(0)
    # # cv.destroyAllwindows()


