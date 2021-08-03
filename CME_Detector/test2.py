import datetime
import time
import cv2
import numpy as np
import calendar
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statistics import median
from PIL import Image, ImageDraw

offset_x = -10
offset_y = -7

def image_load(file_name):
    img = cv2.imread(file_name)
    return img


def image_save(file_name, image_object):
    cv2.imwrite(file_name, image_object)


def polar_to_rectangular(angle, distance):
    image_size = 512
    imagecentre = image_size / 2
    """
    With our image, we have a line at an angle radiating from the centre. We want
    the pixel value at the end. THis method will return the [x,y] co-ords accounting
    for the offset the actual centre point from the geometric centre of the image
    Angle: in degrees measured clockwise from North/top
    Distance: in pixels, as a radius measured from the centre.
    """
    if angle == 0 or angle == 360:
        x = imagecentre
        y = distance

    if angle == 90:
        x = distance
        y = imagecentre

    if angle == 180:
        x = imagecentre
        y = imagecentre + distance

    if angle == 270:
        x = imagecentre - distance
        y = imagecentre

    # finally add the offsets and return
    x = x + offset_x
    y = y + offset_y
    return [x,y]



test = image_load("part1.jpg")