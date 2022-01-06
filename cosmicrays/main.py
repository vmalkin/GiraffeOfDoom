import cv2

if __name__ == '__main__':
    camera = cv2.VideoCapture(2)


    # Can set - no change
    # camera.set(cv2.CAP_PROP_GAIN, 255)

    # camera.set(cv2.CAP_PROP_BRIGHTNESS, 255)
    #
    # # No
    # camera.set(cv2.CAP_PROP_GAMMA, 1)

    # Can set. 255 max value
    camera.set(cv2.CAP_PROP_SATURATION, 100)
    camera.set(cv2.CAP_PROP_HUE, -1)
    camera.set(cv2.CAP_PROP_CONTRAST, 100)
    # Set to zero for auto exposure. Set to 1 for manual exposure
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
    # max of 10000 manually
    camera.set(cv2.CAP_PROP_EXPOSURE, 10)

    # showing values of the properties
    print("CV_CAP_PROP_FRAME_WIDTH: '{}'".format(camera.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print("CV_CAP_PROP_FRAME_HEIGHT : '{}'".format(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("CAP_PROP_FPS : '{}'".format(camera.get(cv2.CAP_PROP_FPS)))
    print("CAP_PROP_POS_MSEC : '{}'".format(camera.get(cv2.CAP_PROP_POS_MSEC)))
    print("CAP_PROP_FRAME_COUNT  : '{}'".format(camera.get(cv2.CAP_PROP_FRAME_COUNT)))
    print("CAP_PROP_BRIGHTNESS : '{}'".format(camera.get(cv2.CAP_PROP_BRIGHTNESS)))
    print("CAP_PROP_CONTRAST : '{}'".format(camera.get(cv2.CAP_PROP_CONTRAST)))
    print("CAP_PROP_SATURATION : '{}'".format(camera.get(cv2.CAP_PROP_SATURATION)))
    print("CAP_PROP_HUE : '{}'".format(camera.get(cv2.CAP_PROP_HUE)))
    print("CAP_PROP_GAIN  : '{}'".format(camera.get(cv2.CAP_PROP_GAIN)))
    print("CAP_PROP_CONVERT_RGB : '{}'".format(camera.get(cv2.CAP_PROP_CONVERT_RGB)))
    print("CAP_PROP_GAMMA : '{}'".format(camera.get(cv2.CAP_PROP_GAMMA)))
    print("CAP_PROP_EXPOSURE : '{}'".format(camera.get(cv2.CAP_PROP_EXPOSURE)))

    while True:
        ret, frame = camera.read()
        # frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        cv2.imshow('Input', frame)

        c = cv2.waitKey(1)
        if c == 27:
            break

    camera.release()
    cv2.destroyAllWindows()