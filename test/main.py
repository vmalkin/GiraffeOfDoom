import cv2

cam  = cv2.VideoCapture(0)

ret, frame = cam.read()

while True:
    ret, frame = cam.read()
    cv2.imshow("Captured", frame)
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyWindow("Captured")
        break

cam.release()
cv2.destroyAllWindows()