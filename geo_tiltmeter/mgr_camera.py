import csv

import cv2
import numpy as np


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

def setup_cam(camera):
    # camera is quickcam C270
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
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_BRIGHTNESS, 120)
    camera.set(cv2.CAP_PROP_CONTRAST, 50)
    # camera.set(cv2.CAP_PROP_HUE, 13)  # 13.0
    # camera.set(cv2.CAP_PROP_SATURATION, 128)
    # camera.set(cv2.CAP_PROP_EXPOSURE, 0)
    # 3 is mode for manual exposure
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3);
    camera.set(cv2.CAP_PROP_GAIN, 0)

def crop_image(image):
    height = image.shape[0]
    width = image.shape[1]
    middle = int(height / 2)
    start_x = 50
    start_y = int(middle - 50)
    end_x = width - 50
    end_y = int(middle + 50)
    cropped_img = image[start_y:end_y, start_x:end_x]
    return cropped_img



cam  = cv2.VideoCapture(0)
setup_cam(cam)
ret, frame1 = cam.read()

while True:
    ret, frame2 = cam.read()
    # diff = cv2.absdiff(frame1, frame2)
    knife_edge = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    # knife_edge = mask_img(knife_edge, mask)
    knife_edge = crop_image(knife_edge)

    # We will take average of each column of pixels in the image to create a 1D array and use this simply calculate
    # the apparent knife-edge position with sub-pixel accuracy
    one_d_array = []
    arr = np.array(knife_edge)
    for i in range(0, arr.shape[1]):
        t = arr[:, i:i+1]
        n = round(np.mean(t, dtype=np.float64), 2)
        one_d_array.append(n)
    #
    # dhdt = []
    # for i in range(1, len(one_d_array)):
    #     d = one_d_array[i] - one_d_array[i - 1]
    #     dhdt.append(d)
    # print(dhdt)

    # The following is just for displaying the averaged knife edge. Dont need to do this if we're trying to calculate
    # a sub-pixel position
    reformat_one_d_array = np.array(one_d_array, dtype=np.uint8).reshape(1, len(one_d_array))
    reformat_one_d_array = cv2.resize(
        reformat_one_d_array,
        (len(one_d_array), 100)
    )
    cv2.imshow("Press q to quit.", reformat_one_d_array)
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyWindow("Captured. Press q to quit.")
        break

    # # Perform sub-pixel estimation of average knife-edge position.
    # with open('knife_edge.csv', 'w') as k:
    #     for line in one_d_array:
    #         k.write(str(line) + '\n')
    # k.close()
    # break

cam.release()
cv2.destroyAllWindows()