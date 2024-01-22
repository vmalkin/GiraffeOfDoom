import glob
import os
import global_config
import mgr_mp4 as make_anim

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


if __name__ == '__main__':
        data = global_config.noaa_image_data
        store = 1
        diffs = 2

        # Make animations
        folder = 'diffs_g'
        img_files = local_file_list_build(folder)
        # a day is roughly 360 images
        img_files = img_files[-360:]
        make_anim.wrapper(img_files, 'diffs_195a')

        folder = 'diffs_b'
        img_files = local_file_list_build(folder)
        # a day is roughly 360 images
        img_files = img_files[-360:]
        make_anim.wrapper(img_files, 'diffs_171a')

        folder = 'diffs_r'
        img_files = local_file_list_build(folder)
        # a day is roughly 360 images
        img_files = img_files[-360:]
        make_anim.wrapper(img_files, 'diffs_284a')

        folder = 'store_b'
        img_files = local_file_list_build(folder)
        # a day is roughly 360 images
        img_files = img_files[-360:]
        make_anim.wrapper(img_files, '171a')


        folder = 'store_g'
        img_files = local_file_list_build(folder)
        # a day is roughly 360 images
        img_files = img_files[-360:]
        make_anim.wrapper(img_files, '195a')

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

