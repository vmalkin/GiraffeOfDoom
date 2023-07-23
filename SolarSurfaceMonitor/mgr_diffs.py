import numpy as np
import os
import glob

pathsep = os.sep

class ImageMaster():
    def __init__(self, namestring, imageshape):
        self.namestring = namestring
        self.imageshape = imageshape
        self.path_red = None
        self.path_green = None
        self.path_blue = None

def local_file_list_build(directory):
    # Builds and returns a list of files contained in the directory.
    # List is sorted into A --> Z order
    dirlisting = []
    path = directory + pathsep + "*.*"
    for name in glob.glob(path):
        name = os.path.normpath(name)
        # seperator = os.path.sep
        # n = name.split(seperator)
        # nn = n[1]
        dirlisting.append(name)
    dirlisting.sort()
    return dirlisting


def wrapper(suvi_dictionary):
    # Start with an empty image list
    # get the file listing from the first key in the dictionary. we only want files in a particular date range

    # THe files all have the same datetime component in the name. if this name does not exist in the image list
    #  create a new image
    # add the filepath to the correct imagelist variable.
    # Else add the filepath to the exiting image list variable.
    # At the end of this, we should have a populated image list with path variables populated.
    imagelist = []



