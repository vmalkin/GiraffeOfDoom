import cv2

current_camera = 0

def camera_setup_c270(cam):
    cam.set(cv2.CAP_PROP_GAIN, 255)
    cam.set(cv2.CAP_PROP_BRIGHTNESS, 120)
    cam.set(cv2.CAP_PROP_SATURATION, 100)
    cam.set(cv2.CAP_PROP_CONTRAST, 32)
    cam.set(cv2.CAP_PROP_SHARPNESS, 255)
    cam.set(cv2.CAP_PROP_EXPOSURE, 120)
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

print("CUrrent camera: ", current_camera)
camera = cv2.VideoCapture(current_camera)
camera_setup_c270(camera)

print("Exposure: ", camera.get(cv2.CAP_PROP_EXPOSURE))
sh_x = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
sh_y = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("Frame size: ", sh_x, sh_y)

ret, image = camera.read()
cv2.imshow('Current image',image)
cv2.waitKey(0)

