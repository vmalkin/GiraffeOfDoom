from PIL import Image


p = "cme_mini.jpg"
q = "cme_plot.jpg"

try:
    pil_image = Image.open(p)
    pil_image.transpose(Image.FLIP_LEFT_RIGHT)
    pil_image.close()
except:
    print(p)


try:
    pil_image = Image.open(q)
    pil_image.transpose(Image.FLIP_LEFT_RIGHT)
    pil_image.close()
except:
    print(q)