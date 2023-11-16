import cv2
import glob
import os

pathsep = os.sep

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

if __name__ == '__main__':
    image_store = 'diffs_r'
    name = 'type_name'


    filelist = local_file_list_build(image_store)
    print('length of file listing:', len(filelist))
    trim_before = 0
    trim_after = -450
    filelist = filelist[trim_before:trim_after]

    # Create mp4 animation
    print("*** Begin movie creation: ", name)
    i = cv2.imread(filelist[0])
    j = i.shape
    width = j[0]
    height = j[1]
    filename = name + ".mp4"
    # Define codec and create a VideoWriter object
    # cv2.VideoWriter_fourcc(*"mp4v") or cv2.VideoWriter_fourcc("m", "p", "4", "v")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(
        filename=filename, fourcc=fourcc, fps=10.0, frameSize=(width, height)
    )

    # Read each image and write it to the video
    for image in filelist:
        # read the image using OpenCV
        frame = cv2.imread(image)
        # Optional step to resize the input image to the dimension stated in the
        # VideoWriter object above
        # frame = cv2.resize(frame, dsize=(400, 400))
        video.write(frame)

    # Exit the video writer
    video.release()
    print('*** End movie creation: ', name)