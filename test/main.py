import cv2

cam  = cv2.VideoCapture(0)

ret, frame1 = cam.read()
frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

while True:
    ret, frame2 = cam.read()
    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(frame1, frame2)
    cv2.imshow("Captured", diff)
    frame1 = frame2.copy()
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyWindow("Captured")
        break

cam.release()
cv2.destroyAllWindows()