import cv2
import numpy as np
from math import sin, cos, radians

# offset values when coronagraph mask support-vane in top-right position
offset_x = 11
offset_y = -4

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
        # print("a == 0")
        x = imagecentre
        y = imagecentre - distance

    if angle > 0:
        if angle < 90:
            # print("0 < a < 90")
            delta_x = distance * sin(radians(angle))
            delta_y = distance * cos(radians(angle))
            x = imagecentre + delta_x
            y = imagecentre - delta_y

    if angle == 90:
        # print("a == 90")
        x = imagecentre + distance
        y = imagecentre

    if angle > 90:
        if angle < 180:
            # print("90 < a < 180")
            angle = angle - 90
            delta_y = distance * sin(radians(angle))
            delta_x = distance * cos(radians(angle))
            x = imagecentre + delta_x
            y = imagecentre + delta_y

    if angle == 180:
        # print("a == 180")
        x = imagecentre
        y = imagecentre + distance

    if angle > 180:
        if angle < 270:
            # print("180 < a < 270")
            angle = angle - 180
            delta_x = distance * sin(radians(angle))
            delta_y = distance * cos(radians(angle))
            x = imagecentre - delta_x
            y = imagecentre + delta_y

    if angle == 270:
        # print("a == 270")
        x = imagecentre - distance
        y = imagecentre

    if angle > 270:
        if angle < 360:
            # print("270 < a < 360")
            angle = angle - 270
            delta_y = distance * sin(radians(angle))
            delta_x = distance * cos(radians(angle))
            x = imagecentre - delta_x
            y = imagecentre - delta_y

    # finally add the offsets and return
    x = int(x + offset_x)
    y = int(y + offset_y)
    return [x,y]


test = image_load("part1.jpg")
greyimg = cv2.cvtColor(test, cv2.COLOR_BGR2GRAY)
pic = cv2.split(greyimg)
pic = pic[0]

t = []
u = []

# the y direction
for i in range(0, 220):
    # the x direction
    for j in range(0, 360):
        coords = polar_to_rectangular(j, i)
        pixelvalue = pic[coords[0], coords[1]]
        u.append(pixelvalue)
    t.append(u)
    u = []

# https://www.geeksforgeeks.org/convert-a-numpy-array-to-an-image/
array = np.array(t)
# print(array.shape)
# array = np.reshape(array, (200, 360))

image_save("testpic.png", array)

