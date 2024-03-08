import glob
import requests
import os
import time

import global_config
import mgr_multicolour_v2 as multicolour
import mgr_multicolour_diff as multidiff

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
        # create multispectral images
        # Files for each datetime, regardless of the wavelength, have the same name
        files = global_config.noaa_image_data
        store = 1
        savefolder_x = global_config.folder_source_images + pathsep + 'store_suvi_false_x'
        savefolder_y = global_config.folder_source_images + pathsep + 'store_suvi_false_y'

        if os.path.exists(savefolder_x) is False:
            os.makedirs(savefolder_x)

        if os.path.exists(savefolder_y) is False:
            os.makedirs(savefolder_y)

        files_blue_x = local_file_list_build(files[0][store])
        files_blue_x = files_blue_x[-360:]
        files_green_x = local_file_list_build(files[1][store])
        files_green_x = files_green_x[-360:]
        files_red_x = local_file_list_build(files[2][store])
        files_red_x = files_red_x[-360:]

        files_blue_y = local_file_list_build(files[0][store])
        files_blue_y = files_blue_y[-360:]
        files_green_y = local_file_list_build(files[1][store])
        files_green_y = files_green_y[-360:]
        files_red_y = local_file_list_build(files[2][store])
        files_red_y = files_red_y[-360:]

        multifilelist_x = []
        for file_b in files_blue_x:
            tmp = []
            tmp.append(file_b)
            b = file_b.split('_')
            start_b = b[6]

            for file_g in files_green_x:
                g = file_g.split('_')
                start_g = g[6]
                if start_g == start_b:
                    tmp.append(file_g)

            for file_r in files_red_x:
                r = file_r.split('_')
                start_r = r[6]
                if start_r == start_b:
                    tmp.append(file_r)

            if len(tmp) == 3:
                multifilelist_x.append(tmp)

        multifilelist_y = []
        for file_b in files_blue_y:
            tmp = []
            tmp.append(file_b)
            b = file_b.split('_')
            start_b = b[6]

            for file_g in files_green_y:
                g = file_g.split('_')
                start_g = g[6]
                if start_g == start_b:
                    tmp.append(file_g)

            for file_r in files_red_y:
                r = file_r.split('_')
                start_r = r[6]
                if start_r == start_b:
                    tmp.append(file_r)

            if len(tmp) == 3:
                multifilelist_y.append(tmp)

        multicolour.wrapper(multifilelist_x, savefolder_x)
        multicolour.wrapper(multifilelist_y, savefolder_y)

        # create multispectral difference images
        # Files for each datetime, regardless of the wavelength, have the same name
        files = global_config.noaa_image_data
        diffs = 2
        savefolder_x = global_config.folder_source_images + pathsep + 'store_suvi_fdiff_x'
        if os.path.exists(savefolder_x) is False:
            os.makedirs(savefolder_x)

        savefolder_y = global_config.folder_source_images + pathsep + 'store_suvi_fdiff_y'
        if os.path.exists(savefolder_y) is False:
            os.makedirs(savefolder_y)

        files_blue_x = local_file_list_build(files[0][diffs])
        files_blue_x = files_blue_x[-360:]
        files_green_x = local_file_list_build(files[1][diffs])
        files_green_x = files_green_x[-360:]
        files_red_x = local_file_list_build(files[2][diffs])
        files_red_x = files_red_x[-360:]

        files_blue_y = local_file_list_build(files[0][diffs])
        files_blue_y = files_blue_y[-360:]
        files_green_y = local_file_list_build(files[1][diffs])
        files_green_y = files_green_y[-360:]
        files_red_y = local_file_list_build(files[2][diffs])
        files_red_y = files_red_y[-360:]

        multifilelist_x = []
        for file_b in files_blue_x:
            tmp = []
            tmp.append(file_b)
            b = file_b.split('_')
            start_b = b[6]

            for file_g in files_green_x:
                g = file_g.split('_')
                start_g = g[6]
                if start_g == start_b:
                    tmp.append(file_g)

            for file_r in files_red_x:
                r = file_r.split('_')
                start_r = r[6]
                if start_r == start_b:
                    tmp.append(file_r)

            if len(tmp) == 3:
                multifilelist_x.append(tmp)

        multifilelist_y = []
        for file_b in files_blue_y:
            tmp = []
            tmp.append(file_b)
            b = file_b.split('_')
            start_b = b[6]

            for file_g in files_green_y:
                g = file_g.split('_')
                start_g = g[6]
                if start_g == start_b:
                    tmp.append(file_g)

            for file_r in files_red_y:
                r = file_r.split('_')
                start_r = r[6]
                if start_r == start_b:
                    tmp.append(file_r)

            if len(tmp) == 3:
                multifilelist_y.append(tmp)

        multicolour.wrapper(multifilelist_x, savefolder_x)
        multicolour.wrapper(multifilelist_y, savefolder_y)
