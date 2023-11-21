import glob
import requests
import os
import time
import mgr_diffs_2 as diffs
import mgr_mp4 as make_anim
import mgr_gif as make_gif
import mgr_multicolour_v2 as multicolour
import mgr_multicolour_diff as multidiff

suvidata = {
    '171': {
        'store': 'store_b',
        'diffs': 'diffs_b',
        'url': 'https://services.swpc.noaa.gov/images/animations/suvi/primary/171/'
    },
    '195': {
        'store': 'store_g',
        'diffs': 'diffs_g',
        'url': 'https://services.swpc.noaa.gov/images/animations/suvi/primary/195/'
    },
    '284': {
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

        # Calculate difference images for each wavelength
        for key in suvidata:
            img_files = local_file_list_build(suvidata[key]['store'])
            img_files = img_files[-360:]
            store_diffs = suvidata[key]['diffs']
            diffs.wrapper(img_files, store_diffs, pathsep, key)

        # create multispectral images
        # Files for each datetime, regardless of the wavelength, have the same name
        files_blue = local_file_list_build('store_b')
        files_blue = files_blue[-360:]
        files_green = local_file_list_build('store_g')
        files_green = files_green[-360:]
        files_red = local_file_list_build('store_r')
        files_red = files_red[-360:]

        multifilelist = []
        for file_b in files_blue:
            tmp = []
            tmp.append(file_b)
            b = file_b.split('_')
            start_b = b[4]

            for file_g in files_green:
                g = file_g.split('_')
                start_g = g[4]
                if start_g == start_b:
                    tmp.append(file_g)

            for file_r in files_red:
                r = file_r.split('_')
                start_r = r[4]
                if start_r == start_b:
                    tmp.append(file_r)
            if len(tmp) == 3:
                multifilelist.append(tmp)

        multicolour.wrapper(multifilelist, 'combined')

        # create multispectral difference images
        # Files for each datetime, regardless of the wavelength, have the same name
        files_blue = local_file_list_build('diffs_b')
        files_blue = files_blue[-360:]
        files_green = local_file_list_build('diffs_g')
        files_green = files_green[-360:]
        files_red = local_file_list_build('diffs_r')
        files_red = files_red[-360:]

        multifilelist = []
        for file_b in files_blue:
            tmp = []
            tmp.append(file_b)
            b = file_b.split(pathsep)
            start_b = b[1]

            for file_g in files_green:
                g = file_g.split(pathsep)
                start_g = g[1]
                if start_g == start_b:
                    tmp.append(file_g)

            for file_r in files_red:
                r = file_r.split(pathsep)
                start_r = r[1]
                if start_r == start_b:
                    tmp.append(file_r)
            if len(tmp) == 3:
                multifilelist.append(tmp)

        multidiff.wrapper(multifilelist, 'combined_diffs')

        # Make animations
        folder = 'diffs_g'
        img_files = local_file_list_build(folder)
        # a day is roughly 360 images
        img_files = img_files[-360:]
        make_anim.wrapper(img_files, 'diffs_195a')
        # make_gif.wrapper(img_files, 'diffs_195A')

        folder = 'diffs_b'
        img_files = local_file_list_build(folder)
        # a day is roughly 360 images
        img_files = img_files[-360:]
        make_anim.wrapper(img_files, 'diffs_171a')
        # make_gif.wrapper(img_files, 'diffs_171A')

        folder = 'diffs_r'
        img_files = local_file_list_build(folder)
        # a day is roughly 360 images
        img_files = img_files[-360:]
        make_anim.wrapper(img_files, 'diffs_284a')
        # make_gif.wrapper(img_files, 'diffs_284A')

        folder = 'store_b'
        img_files = local_file_list_build(folder)
        # a day is roughly 360 images
        img_files = img_files[-360:]
        make_anim.wrapper(img_files, '171a')


        folder = 'store_g'
        img_files = local_file_list_build(folder)
        # a day is roughly 360 images
        img_files = img_files[-360:]
        make_anim.wrapper(img_files, '194a')

        folder = 'store_r'
        img_files = local_file_list_build(folder)
        # a day is roughly 360 images
        img_files = img_files[-360:]
        make_anim.wrapper(img_files, '284a')

        folder = 'combined'
        img_files = local_file_list_build(folder)
        # a day is roughly 360 images
        img_files = img_files[-360:]
        make_anim.wrapper(img_files, '3_colour')

        folder = 'combined_diffs'
        img_files = local_file_list_build(folder)
        # a day is roughly 360 images
        img_files = img_files[-360:]
        make_anim.wrapper(img_files, '3_clr_diffs')

        print("*** All image processing completed")
        finishtime = time.time()
        elapsedminutes = round(((finishtime - starttime) / 60),1)
        print("Processing time:", elapsedminutes)
        sleeptime = 3600
        for i in range(sleeptime, 0, -1):
            j = i % 60
            if j == 0:
                mins_left = int(i / 60)
                reportstring = "Next download in " + str(mins_left) + " minutes"
                print(reportstring)
            time.sleep(1)
