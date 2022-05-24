import requests
import re

url_to_get = "https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/2021/c3/20211022/"
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url_to_get, headers=headers)

r = r.text.split("\n")
#  The response is now delimited on newlines. We can get rid lines to only have the HTML with the images
r = r[13:]
r = r[:-4]

returnlist = []
for line in r:
    l1 = line.split("href=\"")
    l2 = (l1[1])
    l2 = l2.split("\">")
    filename = l2[0]
    if re.search("c3_512", filename):
        returnlist.append(filename)


