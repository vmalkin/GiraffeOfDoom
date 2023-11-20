import glob
import requests
import os
import time
import cv2
# file path seperator / or \ ???
pathsep = os.sep

def wrapper(filelist, name):
    # Create mp4 animation
    print("*** Begin movie creation: ", name)

    # try and get the shape from the first valid image. Skip broken ones
    # for file in filelist:
    #     try:
    #         i = cv2.imread(file)
    #         j = i.shape
    #         break
    #     except:
    #         pass
    #
    # width = j[0]
    # height = j[1]
    # filename = name + ".mp4"
    filename = name + ".webm"
    # Define codec and create a VideoWriter object
    # cv2.VideoWriter_fourcc(*"mp4v") or cv2.VideoWriter_fourcc("m", "p", "4", "v")

    # fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fourcc = cv2.VideoWriter_fourcc('V', 'P', '9', '0')
    video = cv2.VideoWriter(
        # filename=filename, fourcc=fourcc, fps=10.0, frameSize=(width, height)
        filename=filename, fourcc=fourcc, fps=10.0, frameSize=(640, 640)
    )

    # Read each image and write it to the video
    for image in filelist:
        # read the image using OpenCV
        frame = cv2.imread(image)
        # Optional step to resize the input image to the dimension stated in the
        # VideoWriter object above
        try:
            frame = cv2.resize(frame, dsize=(640, 640))
            video.write(frame)
        except cv2.error:
            print('!!! Unable to resize video frame')

    # Exit the video writer
    video.release()
    print('*** End movie creation: ', name)

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
wrapper(img_files, 'diffs_284A')
# make_gif.wrapper(img_files, 'diffs_284A')