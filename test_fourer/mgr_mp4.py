import cv2
import os
import glob

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
        width, height, colourdepth = image.shape
        tracker_length = int(image_number / list_length * width)
        cv2.line(image, (0, height - 5), (tracker_length, height - 5), (0, 0, 255), 5)
    except:
        print('Unable to process image for animation tracker: ', image)
    return image


def wrapper():
    # Make animations
    folder = "movies"
    img_files = local_file_list_build("images")
    outputfile = folder + os.sep + 'fourier'

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

    width = j[0]
    height = j[1]

    filename_mp4 = outputfile + ".mp4"
    # filename_web = outputfile + ".webm"

    # Define codec and create a VideoWriter object
    fourcc_mp4 = cv2.VideoWriter_fourcc(*"mp4v")
    # fourcc_web = cv2.VideoWriter_fourcc('V', 'P', '8', '0')


    video_mp4 = cv2.VideoWriter(
        # filename=filename, fourcc=fourcc, fps=10.0, frameSize=(width, height)
        filename=filename_mp4, fourcc=fourcc_mp4, fps=10.0, frameSize=(width, height)
    )

    # video_web = cv2.VideoWriter(
    #     # filename=filename, fourcc=fourcc, fps=10.0, frameSize=(width, height)
    #     filename=filename_web, fourcc=fourcc_web, fps=10.0, frameSize=(640, 640)
    # )

    # Read each image and write it to the video
    for i in range(0, len(img_files)):
        print("building video: ", i)
        # read the image using OpenCV
        frame_mp4 = cv2.imread(img_files[i])
        # frame_web = cv2.imread(img_files[i])

        frame_mp4 = make_animation_tracker(frame_mp4, len(img_files), i)
        # frame_web = make_animation_tracker(frame_web, len(img_files), i)

        # Optional step to resize the input image to the dimension stated in the
        # VideoWriter object above
        try:
            # frame_web = cv2.resize(frame_web, dsize=(640, 640))
            video_mp4.write(frame_mp4)
            # video_web.write(frame_web)
        except cv2.error:
            print('!!! Unable to resize video frame')

    # Exit the video writer
    # video_web.release()
    video_mp4.release()

    print('*** End movie creation: ', outputfile)

if __name__ == '__main__':
    wrapper()