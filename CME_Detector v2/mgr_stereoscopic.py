import os
from PIL import Image

stereo = "stereoscopic"
if os.path.exists(stereo) is False:
    os.makedirs(stereo)


def wrapper(directory):
    # create video of the last 24 hours from the enhanced folder.
    # approx no of images in a day is 30 for the enhanced folder!
    stereoarray = []
    imagelist = os.listdir(directory)
    imagelist.sort()
    truncate = 60
    if len(imagelist) > truncate:
        imagelist = imagelist[-truncate:]
    imagelist.sort()
    filepath = directory + "/" + imagelist[0]
    img1 = Image.open(filepath)
    for i in range(1, len(imagelist)):
        sf = imagelist[i].split(".")
        stereo_filename = sf[0]
        filepath = directory + "/" + imagelist[i]
        img2 = Image.open(filepath)
        w = img2.width
        h = img2.height
        stereoimage = Image.new("RGB", [w*2, h])
        stereoimage.paste(img1)
        stereoimage.paste(img2, (img2.size[0], 0))
        stereoarray.append(stereoimage)
        savefile = stereo + "/" + stereo_filename + ".jpg"
        stereoimage.save(savefile)
        img1 = img2

    stereoarray[0].save("stereo_cme.gif",
                      format="GIF",
                      save_all=True,
                      append_images=stereoarray[1:],
                      duration=150,
                      loop=0)
