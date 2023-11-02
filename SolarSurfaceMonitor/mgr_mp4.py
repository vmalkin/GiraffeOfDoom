import cv2
def wrapper(filelist, name):
    print('*** BEGIN MP4', name)
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
        # frame = cv2.resize(frame, dsize=(width, height))
        video.write(frame)

    # Exit the video writer
    video.release()
    print('*** END MP4')