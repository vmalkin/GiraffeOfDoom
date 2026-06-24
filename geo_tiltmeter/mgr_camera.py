import cv2
import numpy as np
from time import sleep
from math import tan, radians





# def make_dynamic_mask_segment(image):
#     mask = np.zeros(image.shape[:2], dtype="uint8")
#     dimensions = mask.shape
#     height = image.shape[0]
#     width = dimensions[1]
#     middle = int(height / 2)
#
#     start_x = 0
#     start_y = int(middle - 120)
#     end_x = width
#     end_y = int(middle + 120)
#
#     # The color is specified in BGR, not RGB (OpenCV default).
#     cv2.rectangle(mask, (start_x, start_y), (end_x, end_y), (255, 255, 255), -1)
#     return mask

def setup_cam():
    # Manually set camera parameters to prevent varion due to automatic functions.
    # Field of View (FOV) 	60°
    # Focal Length 	4.0 mm
    # Optical Resolution (True) 	1280 x 960 1.2MP
    # Image Capture (4:3 SD) 	320x240, 640x480 1.2 MP, 3.0 MP
    # Image Capture (16:9 W) 	360p, 480p, 720p
    # Video Capture (4:3 SD) 	320x240, 640x480, 800x600
    # Video Capture (16:9 W) 	360p, 480p, 720p,
    # Frame Rate (max) 	30fps @ 640x480
    # Change the camera setting using the set() function
    print(cv2.CAP_PROP_XI_DEVICE_SN)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cam.set(cv2.CAP_PROP_GAIN, 0)
    cam.set(cv2.CAP_PROP_BRIGHTNESS, 120)
    cam.set(cv2.CAP_PROP_CONTRAST, 50)
    # cam.set(cv2.CAP_PROP_HUE, 13)  # 13.0
    # cam.set(cv2.CAP_PROP_SATURATION, 128)
    cam.set(cv2.CAP_PROP_EXPOSURE, 0)
    cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0);

def crop_image(image):
    # mask = np.zeros(image.shape[:2], dtype="uint8")
    # dimensions = mask.shapeq
    height = image.shape[0]
    width = image.shape[1]
    middle = int(height / 2)
    #
    start_x = 50
    start_y = int(middle - 50)
    end_x = width - 50
    end_y = int(middle + 50)
    #
    # # The color is specified in BGR, not RGB (OpenCV default).
    # cv2.rectangle(mask, (start_x, start_y), (end_x, end_y), (255, 255, 255), -1)
    cropped_img = image[start_y:end_y, start_x:end_x]
    return cropped_img



# def mask_img(image_to_process, maskname):
#     outputimg = cv2.bitwise_and(image_to_process, image_to_process, mask=maskname)
#     return outputimg
cam  = cv2.VideoCapture(1)
ret, frame1 = cam.read()
# setup_cam()

ret, frame1 = cam.read()
# mask = make_dynamic_mask_segment(frame1)
while True:
    ret, frame2 = cam.read()
    # diff = cv2.absdiff(frame1, frame2)
    knife_edge = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    # knife_edge = mask_img(knife_edge, mask)
    knife_edge = crop_image(knife_edge)

    # # Adjust the brightness and contrast
    # # g(i,j)=α⋅f(i,j)+β
    # # alpha < 0 reduce. Alpha = 1 is original value.
    # # beta ∈ [-255, 255]
    # # control Contrast by 1.5
    # alpha = 1
    # # control brightness by 5q0
    # beta = 0
    # knife_edge = cv2.convertScaleAbs(knife_edge, alpha=alpha, beta=beta)

    # # We will take average of each column of pixels in the image to create a 1D array and use this simply calculate
    # # the apparent knife-edge position with sub-pixel accuracy
    # one_d_array = []
    # arr = np.array(knife_edge)
    # for i in range(0, arr.shape[1]):
    #     t = arr[:, i:i+1]
    #     n = round(np.mean(t, dtype=np.float64), 2)
    #     one_d_array.append(n)

    # # gradient = np.gradient(one_d_array)
    # # for item in one_d_array:
    # #     print(item)
    # # break
    # i = np.array(one_d_array, dtype=np.uint8).reshape(1, 640)
    # i = cv2.resize(
    #     i,
    #     (640, 200),
    #     interpolation=cv2.INTER_NEAREST
    # )
    cv2.imshow("Press q to quit.", knife_edge)
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyWindow("Captured. Press q to quit.")
        break


cam.release()
cv2.destroyAllWindows()