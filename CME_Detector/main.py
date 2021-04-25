import cv2
import urllib.request
import time

url_lasco_c3 = "https://soho.nascom.nasa.gov/data/realtime/c3/512/latest.jpg"
t = int(time())
img_latest = "lasco.jpg"

try:
    request = urllib.request.Request(url_lasco_c3, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(request, timeout=10)
    with open(img_latest, 'wb') as f:
        f.write(response.read())
except urllib.request.HTTPError:
    # logging.error("Unable to load/save image from URL: " + str(imageurl) + " " + str(filename))
    print("unable to load image")
