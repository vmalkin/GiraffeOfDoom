import cv2
import numpy as np
from math import tan, radians

# Field of View (FOV) 	60°
# Focal Length 	4.0 mm
# Optical Resolution (True) 	1280 x 960 1.2MP
# Image Capture (4:3 SD) 	320x240, 640x480 1.2 MP, 3.0 MP
# Image Capture (16:9 W) 	360p, 480p, 720p
# Video Capture (4:3 SD) 	320x240, 640x480, 800x600
# Video Capture (16:9 W) 	360p, 480p, 720p,
# Frame Rate (max) 	30fps @ 640x480
height = 480
width = 640
resolution= 60 / height

cam  = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
ret, frame1 = cam.read()

print(f'Image dimensions: {frame1.shape}. Resolution is {resolution} degrees per pixel')
print(f'movement resolution.')
theta = radians(resolution)
tan_theta = tan(theta)
print(f'At 1m = {round(tan_theta * 1000, 0)}mm.')
print(f'At 2m = {round(tan_theta * 2000, 0)}mm.')
print(f'At 5m = {round(tan_theta * 5000, 0)}mm.')
print(f'At 10m = {round(tan_theta * 10000, 0)}mm.')
print(f'At 20m = {round(tan_theta * 20000, 0)}mm.')
print(f'At 50m = {round(tan_theta * 50000, 0)}mm.')
print(f'At 100m = {round(tan_theta * 100000, 0)}mm.')



# new_image = np.zeros(frame1.shape, frame1.dtype)

while True:
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame1, frame2)
    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Adjust the brightness and contrast
    # g(i,j)=α⋅f(i,j)+β
    # alpha < 0 reduce. Alpha = 1 is original value.
    # beta ∈ [-255, 255]
    # control Contrast by 1.5
    alpha = 2
    # control brightness by 50
    beta = 50
    diff = cv2.convertScaleAbs(diff, alpha=alpha, beta=beta)

    # # Create the sharpening kernel
    # kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    # # Sharpen the image
    # diff = cv2.filter2D(diff, -1, kernel)

    # # gaussian blur
    # diff = cv2.GaussianBlur(diff, (3, 3), 0)

    # cv2.imshow("Cam", frame2)
    cv2.imshow("Diff Image", diff)
    frame1 = frame2.copy()
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyWindow("Captured")
        break

cam.release()
cv2.destroyAllWindows()