import cv2
import numpy as np

class PictureToProcess:
    def __init__(self, picturefilename):
        self.imagename = picturefilename
        self.img = self._image_read(picturefilename)
        self.pixelvalues = self._return_pixelvalue(self.img)

    def _image_read(self, filename):
        img = cv2.imread(filename)
        return img

    def _return_pixelvalue(self, img):
        img_height = img.shape[0]
        img_width = img.shape[1]
        pxl = img[int(img_height / 2),int(img_width / 2)]
        # array in format [blue, green, red]. closer to zero, closer to black
        return pxl

if __name__ == "__main__":
    filelist = ["00-20-49-66utc.png",
                "01-06-54-31utc.png",
                "07-38-27-44utc.png",
                "10-57-31-98utc.png",
                "11-04-31-59utc.png",
                "11-33-30-38utc.png",
                "15-18-09-58utc.png",
                "15-21-49-77utc.png",
                "15-26-38-77utc.png",
                "16-04-40-03utc.png",
                "red.png"]

    picturelist = []
    for item in filelist:
        pic = PictureToProcess(item)
        picturelist.append(pic)

    for pic in picturelist:
        print(pic.pixelvalues)

