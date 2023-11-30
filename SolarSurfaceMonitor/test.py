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

def getfilename(pathname):
    p = pathname.split(pathsep)
    pp = p[1].split('_')
    return pp[0]


folder = 'diffs_g'
img_files = local_file_list_build(folder)
# a day is roughly 360 images
img_files = img_files[-360:]

returnarray = []
for item in img_files:
    tmp = []
    img = cv2.imread(item)
    result = np.histogram(img, bins=5, range=(0, 256))
    # result[0] is histogram, result[1] is datatype, result[2] are bin labels
    histgm = (result[0])
    tmp.append(getfilename(item))
    tmp.append(histgm[0])
    tmp.append(histgm[4])
    returnarray.append(tmp)

returnarray = np.array(returnarray)
# returnarray = np.array(returnarray)

# numpy.ndarray.astype
pixels_black = returnarray[:,1]
pixels_white = returnarray[:,2]

# std_wh = np.std(pixels_white)
# std_bl = np.std(pixels_black)
# avg_wh = np.average(pixels_white)
# avg_bl = np.average(pixels_black)
# with open('histograms.csv', 'w') as h:
#     for line in returnarray:
#         d = line[0] + ',' + str(line[1]) + ',' + str(line[2]) + str(average1) + str(average2) + str(std1) + str(std2)
#         d = line + '\n'
#         h.write(str(d))
# h.close()




# make_anim.wrapper(img_files, '3_clr_diffs')