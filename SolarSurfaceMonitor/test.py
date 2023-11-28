import glob
import os
import cv2
import numpy as np

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


folder = 'diffs_r'
img_files = local_file_list_build(folder)
# a day is roughly 360 images
img_files = img_files[-360:]

returnarray = []
for item in img_files:
    dp = ''
    img = cv2.imread(item)
    result = np.histogram(img, bins=10, range=(0, 256))
    # result[0] is histogram, result[1] is datatype, result[2] are bin labels
    histgm = (result[0])
    for item in histgm:
        dp = dp + ',' + str(item)
    returnarray.append(dp)

with open('histograms.csv', 'w') as h:
    for line in returnarray:
        d = line + '\n'
        h.write(str(d))
h.close()




# make_anim.wrapper(img_files, '3_clr_diffs')