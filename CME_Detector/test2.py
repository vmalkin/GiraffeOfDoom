import cv2
import numpy as np
from PIL import Image as im
from math import sin, cos, radians

offset_x = 0
offset_y = 0
image_size = 512
imagecentre = image_size / 2

def image_load(file_name):
    img = cv2.imread(file_name)
    return img


def image_save(file_name, image_object):
    cv2.imwrite(file_name, image_object)


def polar_to_rectangular(angle, distance):
    """
    With our image, we have a line at an angle , radiating from
    the centre. We want the pixel value at the end. THis method will return the [x,y] co-ords accounting
    for the offset the actual centre point from the geometric centre of the image

    Angle: in degrees measured clockwise from North/top
    Distance: in pixels, as a radius measured from the centre.
    """
    if angle == 0 or angle == 360:
        x = imagecentre
        y = imagecentre - distance

    if angle > 0:
        if angle < 90:
            delta_x = distance * sin(radians(angle))
            delta_y = distance * cos(radians(angle))
            x = imagecentre + delta_x
            y = imagecentre - delta_y

    if angle == 90:
        x = imagecentre + distance
        y = imagecentre

    if angle > 90:
        if angle < 180:
            angle = angle - 90
            delta_y = distance * sin(radians(angle))
            delta_x = distance * cos(radians(angle))
            x = imagecentre + delta_x
            y = imagecentre + delta_y

    if angle == 180:
        x = imagecentre
        y = imagecentre + distance

    if angle > 180:
        if angle < 270:
            angle = angle - 180
            delta_x = distance * sin(radians(angle))
            delta_y = distance * cos(radians(angle))
            x = imagecentre - delta_x
            y = imagecentre + delta_y

    if angle == 270:
        x = imagecentre - distance
        y = imagecentre

    if angle > 270:
        if angle < 360:
            angle = angle - 270
            delta_x = distance * sin(radians(angle))
            delta_y = distance * cos(radians(angle))
            x = imagecentre - delta_x
            y = imagecentre - delta_y

    # finally add the offsets and return
    x = int(x + offset_x)
    y = int(y + offset_y)
    return [x,y]


test = image_load("part2.jpg")
greyimg = cv2.cvtColor(test, cv2.COLOR_BGR2GRAY)
pic = cv2.split(greyimg)
pic = pic[0]

t = []
for i in range(0, 201):
    for j in range(0, 361):
        coords = polar_to_rectangular(j, 1)
        t.append(pic[coords[0], coords[1]])

# https://www.geeksforgeeks.org/convert-a-numpy-array-to-an-image/
array = np.arange(0, 72000, 1, np.uint8)
print(array.shape)
array = np.reshape(array, (200, 360))
testpic = im.fromarray(array)
testpic.save('testpic.png')

cv2.imshow("Test", testpic)
cv2.waitKey(0) # waits until a key is pressed
cv2.destroyAllWindows() # destroys the window showing image
