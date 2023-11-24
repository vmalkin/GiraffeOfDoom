import cv2
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
    filename1 = name + ".mp4"
    filename = name + ".webm"
    # Define codec and create a VideoWriter object
    # cv2.VideoWriter_fourcc(*"mp4v") or cv2.VideoWriter_fourcc("m", "p", "4", "v")
    fourcc1 = cv2.VideoWriter_fourcc(*"mp4v")
    fourcc = cv2.VideoWriter_fourcc('V', 'P', '8', '0')
    video = cv2.VideoWriter(
        # filename=filename, fourcc=fourcc, fps=10.0, frameSize=(width, height)
        filename=filename, fourcc=fourcc, fps=10.0, frameSize=(640, 640)
    )

    video1 = cv2.VideoWriter(
        # filename=filename, fourcc=fourcc, fps=10.0, frameSize=(width, height)
        filename=filename1, fourcc=fourcc1, fps=10.0, frameSize=(640, 640)
    )

    # Read each image and write it to the video
    for image in filelist:
        # read the image using OpenCV
        frame = cv2.imread(image)
        # Optional step to resize the input image to the dimension stated in the
        # VideoWriter object above
        try:
            frame = cv2.resize(frame, dsize=(640, 640))
            video1.write(frame)
            video.write(frame)
        except cv2.error:
            print('!!! Unable to resize video frame')

    # Exit the video writer
    video1.release()
    video.release()
    print('*** End movie creation: ', name)