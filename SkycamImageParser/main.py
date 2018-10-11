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


def imgtag(filename, index_value, img_list, del_list):
    index_value = str(index_value)
    appendstring = r'<div id="img' + index_value + r'"><img src="' + filename + r'"><p>' + filename + r'<br><br>'
    appendstring = appendstring + r'<button onclick="img' + index_value + r'()">Keep this file</button>'
    appendstring = appendstring + r'<script type="text/javascript"> function img' + index_value + r'()'
    appendstring = appendstring + r'document.getElementById("del' + index_value + r'").style.display = "none";'
    appendstring = appendstring + r'document.getElementById("img' + index_value + r'").style.backgroundColor="#009000";'
    appendstring = appendstring + r'}</script></div>'
    appendstring = appendstring + '\n'
    img_html.append(appendstring)

    delstring = r'<div id="del' + index_value + r'">del ' + filename + r'</div>'
    delstring = delstring + '\n'
    del_list.append(delstring)




if __name__ == "__main__":
    try:
        os.remove("images.html")
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

    img_html = []
    del_html = []

    for i in range(0, len(picturelist)):
        # print(pic.imagename + " " + pic.pixelvalues)
        rd = int(picturelist[i].pixelvalues[0])
        gr = int(picturelist[i].pixelvalues[1])
        bl = int(picturelist[i].pixelvalues[2])

        # sodium light pollution on clouds at night
        if  rd >= gr > bl:
            print(picturelist[i].imagename + " Light pollution at night")
            imgtag(picturelist[i].imagename, i, img_html, del_html)

        # high cloud
        threshold = 140
        if rd > threshold:
            if gr > threshold:
                if bl > threshold:
                    print(picturelist[i].imagename + " Overcast sky")
                    imgtag(picturelist[i].imagename, i, img_html, del_html)
        
