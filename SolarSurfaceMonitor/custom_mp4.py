import glob
import os
import mgr_mp4 as make_anim

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

folder = 'custom'
img_files = local_file_list_build(folder)
# a day is roughly 360 images
img_files = img_files[-360:]
make_anim.wrapper(img_files, 'custom')