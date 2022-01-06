import cv2

if __name__ == '__main__':
    camera = cv2.VideoCapture(2)
    camera.set(cv2.CAP_PROP_EXPOSURE, 2)

    while True:
        ret, frame = camera.read()
        # frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        cv2.imshow('Input', frame)

        c = cv2.waitKey(1)
        if c == 27:
            break

    camera.release()
    cv2.destroyAllWindows()