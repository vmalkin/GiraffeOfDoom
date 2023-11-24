import cv2
import glob
import requests
import os
import time

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


def wrapper(filelist, name):
    # Create mp4 animation
    print("*** Begin movie creation: ", name)

    # try and get the shape from the first valid image. Skip broken ones
    for file in filelist:
        try:
            i = cv2.imread(file)
            j = i.shape
            break
        except:
            pass

    width = j[0]
    height = j[1]

    filename_mp4 = name + ".mp4"
    filename_web = name + ".webm"

    # Define codec and create a VideoWriter object
    fourcc_mp4 = cv2.VideoWriter_fourcc(*"mp4v")
    fourcc_web = cv2.VideoWriter_fourcc('V', 'P', '8', '0')


    video_mp4 = cv2.VideoWriter(
        # filename=filename, fourcc=fourcc, fps=10.0, frameSize=(width, height)
        filename=filename_mp4, fourcc=fourcc_mp4, fps=10.0, frameSize=(width, height)
    )

    video_web = cv2.VideoWriter(
        # filename=filename, fourcc=fourcc, fps=10.0, frameSize=(width, height)
        filename=filename_web, fourcc=fourcc_web, fps=10.0, frameSize=(640, 640)
    )

    # Read each image and write it to the video
    for image in filelist:
        # read the image using OpenCV
        frame_mp4 = cv2.imread(image)
        frame_web = cv2.imread(image)
        # Optional step to resize the input image to the dimension stated in the
        # VideoWriter object above
        try:
            frame_web = cv2.resize(frame_web, dsize=(640, 640))
            video_mp4.write(frame_mp4)
            video_web.write(frame_web)
        except cv2.error:
            print('!!! Unable to resize video frame')

    # Exit the video writer
    video_web.release()
    video_mp4.release()

    print('*** End movie creation: ', name)

folder = 'diffs_g'
img_files = local_file_list_build(folder)
# a day is roughly 360 images
img_files = img_files[-360:]
wrapper(img_files, 'diffs_195a')
# make_gif.wrapper(img_files, 'diffs_195A')