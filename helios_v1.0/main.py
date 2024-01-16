import glob
import requests
import os
import time



suvidata = {
    '171': {
        'title': '',
        'store': 'store_b',
        'diffs': 'diffs_b',
        'url': 'https://services.swpc.noaa.gov/images/animations/suvi/primary/171/'
    },
    '195': {
        'title': '',
        'store': 'store_g',
        'diffs': 'diffs_g',
        'url': 'https://services.swpc.noaa.gov/images/animations/suvi/primary/195/'
    },
    '284': {
        'title': '',
        'store': 'store_r',
        'diffs': 'diffs_r',
        'url': 'https://services.swpc.noaa.gov/images/animations/suvi/primary/284/'
    }
}

# file path seperator / or \ ???
pathsep = os.sep


def local_file_list_build(directory):
    # Builds and returns a list of files contained in the directory.
    # List is sorted into A --> Z order
    dirlisting = []
    path = directory + pathsep + "*.*"
    for name in glob.glob(path):
        name = os.path.normpath(name)
        dirlisting.append(name)
    dirlisting.sort()
    return dirlisting


def get_resource_from_url(url_to_get):
    response = ""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url_to_get, headers=headers)
    except:
        print('unable to load URL', url_to_get)
        print('Try: pip install --upgrade certifi')
    return response


def parseimages(listofimages, imagestore):
    set_downloads = set(listofimages)
    stored = os.listdir(imagestore)
    set_stored = set(stored)
    newfiles = set_downloads.difference(set_stored)
    return newfiles


def downloadimages(img_url, listofimages, storagelocation):
    for img in listofimages:
        file = storagelocation + pathsep + img
        img1url = img_url + img
        if os.path.exists(file) is False:
            response1 = get_resource_from_url(img1url)
            print('Saving file ', file)
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

    r = r[9:]
    r = r[:-3]

    # Now split the lines around image file names. Return only the ones 512 in size
    returnlist = []
    for line in r:
        l = line.split('href=')
        l1 = l[1].split('>or_suvi')
        f = l1[0][1:-1]
        returnlist.append(f)
    return returnlist


def playbell():
    # Ring the system bell
    pass


def download_suvi(lasco_url, storage_folder):
    print(lasco_url)
    listofimages = get_imagelist(lasco_url)
    newimages = parseimages(listofimages, storage_folder)
    if len(newimages) > 0:
        # rings the terminal bell
        print("\a")
        playbell()
        downloadimages(lasco_url, newimages, storage_folder)


if __name__ == '__main__':
    print('*** BEGIN image download from sources...')
    for key in suvidata:
        if os.path.exists(suvidata[key]['store']) is False:
            os.makedirs(suvidata[key]['store'])

        if os.path.exists(suvidata[key]['diffs']) is False:
            os.makedirs(suvidata[key]['diffs'])

    while True:
        starttime = time.time()
        # get the latest SUVI images
        for key in suvidata:
            download_suvi(suvidata[key]['url'], suvidata[key]['store'])
            print('*** Downloads completed')

        print("*** All image downloading COMPLETED")
