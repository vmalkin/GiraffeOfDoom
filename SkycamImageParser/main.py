import cv2


# ##############
# M E T H O D S
# ##############
def _image_read(self, file_name):
    img = cv2.imread(file_name)
    return img