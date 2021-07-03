import cv2
import numpy as np

if __name__ == "__main__":
    image_lasco = "c://temp//lasco.jpg"
    image_stereo_a = "c://temp//stereo_a.jpg"

    img_l = cv2.imread(image_lasco)
    img_s = cv2.imread(image_stereo_a)

    # crop and scale images to have the same FOV
    # convert to gray scale
    # erode and dialate to smooth images.
    # Apply any other contrast/brightness to have images the same intensity
    # Create 3D point cloud of intersecting volume. Normalise the intensities to fit 0-254
