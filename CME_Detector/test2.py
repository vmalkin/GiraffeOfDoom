import datetime
import time
import cv2
import numpy as np
import calendar
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statistics import median
from PIL import Image, ImageDraw

def image_load(file_name):
    img = cv2.imread(file_name)
    return img


def image_save(file_name, image_object):
    cv2.imwrite(file_name, image_object)


test = image_load("part1.jpg")