import cv2
import os
import glob
import constants as k

def local_file_list_build(directory):
    # Builds and returns a list of files contained in the directory.
    # List is sorted into A --> Z order
    dirlisting = []
    path = directory + os.sep + "*.*"
    for name in glob.glob(path):
        name = os.path.normpath(name)
        dirlisting.append(name)
    dirlisting.sort()
    return dirlisting


def make_animation_tracker(image, list_length, image_number):
    try:
        height, width, colourdepth = image.shape
        tracker_length = int(image_number / list_length * width)
        cv2.line(image, (0, height - 5), (tracker_length, height - 5), (0, 0, 255), 5)
    except:
        print('Unable to process image for animation tracker: ', image)
    return image


def wrapper():
    # Make animations
    folder = k.movie_dir
    img_files = local_file_list_build(k.img_dir)
    print(img_files)
    outputfile = folder + os.sep + 'fourier.mp4'

    # Create mp4 animation
    print("*** Begin movie creation: ", outputfile)

    # try and get the shape from the first valid image. Skip broken ones
    for file in img_files:
        try:
            i = cv2.imread(file)
            j = i.shape
            break
        except:
            pass
    print(j)
    width = j[1]
    height = j[0]

    filename_mp4 = outputfile
    # Define codec and create a VideoWriter object
    fourcc_mp4 = cv2.VideoWriter_fourcc(*"mp4v")
    video_mp4 = cv2.VideoWriter(filename=filename_mp4, fourcc=fourcc_mp4, fps=30.0, frameSize=(width, height))

    # Read each image and write it to the video
    for i in range(0, len(img_files)):
        frame_mp4 = cv2.imread(img_files[i])
        frame_mp4 = make_animation_tracker(frame_mp4, len(img_files), i)

        try:
            video_mp4.write(frame_mp4)
        except cv2.error:
            print('!!! Unable to add video frame')

    video_mp4.release()
    print('*** End movie creation: ', outputfile)

if __name__ == '__main__':
    wrapper()