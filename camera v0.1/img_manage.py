import datetime
import time
import os
import shutil
import random
import PIL
from PIL import Image

# This function downsizes the image to quicker uploading, using Pillow
def downscale_upload():
    publish_dir = "c:\temp\"
    try:
        img = Image.open("timestamped.png")
        img = img.resize((800, 600), PIL.Image.ANTIALIAS)
        publishimg = publish_dir + "downscaled.png"
        img.save(publishimg, quality=75)
    except:
        print("Unable to open timestamped image")

while True:
    dt = datetime.datetime.utcnow()
    logdate = datetime.datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S-%f')[:-4]

    # THis is the file to be copied
    img_file = "timestamped.png"

    # split the logdate string into two parts (Look at format above) The date is the directory, the time is the file)
    logdate = logdate.split(" ")

    img_dir = logdate[0] + "utc"
    img_name = img_dir + "\\" + logdate[1] + "utc.png"

    if not os.path.exists(img_dir):
        try:
            os.makedirs(img_dir)
            print("image log directory created.")
        except:
            if not os.path.isdir(img_dir):
                print("Unable to create log directory")

    try:
        shutil.copy(img_file, img_name)
        print("Img copied: " + img_name)
        downscale_upload()
    except shutil.Error as e:
        print('Error: %s' % e)

    rand = random.randint(0,10)
    sleep_interval = 180 + rand
    time.sleep(sleep_interval)
