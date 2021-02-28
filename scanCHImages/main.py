from PIL import Image
import datetime

file_path = "images"

def posix2utc(posixtime, timeformat):
    # '%Y-%m-%d %H:%M'
    utctime = datetime.datetime.utcfromtimestamp(int(posixtime)).strftime(timeformat)
    return utctime


if __name__ == '__main__':

    file_list = file_path + "//" + "files.txt"

    with open(file_list, "r") as f:
        with open("output.csv", "a") as o:
            counter = 0
            o.write("UTC, wh, bl\n" )

            for line in f:
                img_file = line.split(".jpg")
                psx = img_file[0]
                psx = posix2utc(psx, "%Y-%m-%d %H:%M")
                img_file = file_path + "//" + img_file[0] + ".jpg"

                i = Image.open(img_file)

                colour_bl = 0
                colour_wh = 0
                for pixel in i.getdata():
                    if pixel == 0:
                        colour_bl = colour_bl + 1
                    if pixel == 255:
                        colour_wh = colour_wh + 1
                dp = psx + "," + str(colour_wh) + "," + str(colour_bl)
                o.write(dp + "\n")
                counter +=1
                print(counter)

            o.close()

