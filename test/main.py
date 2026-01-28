import cv2
import numpy as np

# Optical Resolution (True) 	1280 x 960 1.2MP
# Image Capture (4:3 SD) 	320x240, 640x480 1.2 MP, 3.0 MP
# Image Capture (16:9 W) 	360p, 480p, 720p
# Video Capture (4:3 SD) 	320x240, 640x480, 800x600
# Video Capture (16:9 W) 	360p, 480p, 720p,
# Frame Rate (max) 	30fps @ 640x480

cam  = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
ret, frame1 = cam.read()
print(f'Image dimensions: {frame1.shape}')
# new_image = np.zeros(frame1.shape, frame1.dtype)

while True:
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame1, frame2)
    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Adjust the brightness and contrast
    # g(i,j)=α⋅f(i,j)+β
    # control Contrast by 1.5
    alpha = 1.7
    # control brightness by 50
    beta = 20
    diff = cv2.convertScaleAbs(diff, alpha=alpha, beta=beta)

    # # Create the sharpening kernel
    # kernel = np.array([[0, -1, 0], [-1, 2, -1], [0, -1, 0]])
    # # Sharpen the image
    # diff = cv2.filter2D(diff, -1, kernel)

    # gaussian blur
    diff = cv2.GaussianBlur(diff, (3, 3), 0)

    cv2.imshow("Cam", frame2)
    cv2.imshow("Diff Image", diff)
    frame1 = frame2.copy()
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyWindow("Captured")
        break

cam.release()
cv2.destroyAllWindows()