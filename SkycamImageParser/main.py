import cv2
import os


class PictureToProcess:
    def __init__(self, picturefilename):
        self.imagename = picturefilename
        self.img = self._image_read(picturefilename)
        self.pixelvalues = self._return_pixelvalue(self.img)

    def _image_read(self, filename):
        img = cv2.imread(filename)
        return img

    def _return_pixelvalue(self, img):
        swatch_width = 10
        img_height = img.shape[0]
        img_width = img.shape[1]
        x_start = int(img_height / 2)
        y_start = int(img_width / 2)

        # array in format [blue, green, red]. closer to zero, closer to black
        swatch = img[x_start:x_start + swatch_width, y_start:y_start + swatch_width]
        returnvalue = cv2.mean(swatch)
        returnlist = []
        returnlist.append(returnvalue[2])
        returnlist.append(returnvalue[1])
        returnlist.append(returnvalue[0])
        return returnlist


def imgtag(filename):
    with open("images.html", "a") as html:
        appendstring = r'<div><img style = "width: 30%;" src="' + filename + '">' + '<p>' + filename + "<br><br></div>"
        html.write(appendstring + "\n")

def delfile(filename):
    with open("delete_files.bat", "a") as d:
        appendstring = "delete " + filename
        d.write(appendstring + "\n")

if __name__ == "__main__":
    try:
        os.remove("images.html")
        os.remove("delete_files.bat")
    except:
        pass

    filelist = []
    with open("files.txt", "r") as f:
        for line in f:
            line = line.strip()
            filelist.append(line)

    picturelist = []
    for item in filelist:
        try:
            pic = PictureToProcess(item)
            picturelist.append(pic)
        except:
            print("ERROR in parsing image")

    for pic in picturelist:
        # print(pic.imagename + " " + pic.pixelvalues)
        rd = int(pic.pixelvalues[0])
        gr = int(pic.pixelvalues[1])
        bl = int(pic.pixelvalues[2])

        # sodium light pollution on clouds at night
        if  rd >= gr > bl:
            print(pic.imagename + " Light pollution at night")
            imgtag(pic.imagename)
            delfile(pic.imagename)

        # high cloud
        threshold = 140
        if rd > threshold:
            if gr > threshold:
                if bl > threshold:
                    print(pic.imagename + " Overcast sky")
                    imgtag(pic.imagename)
                    delfile(pic.imagename)
