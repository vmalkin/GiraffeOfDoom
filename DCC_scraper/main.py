from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://www.dunedin.govt.nz/search?query=heritage&sort=date"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")

soup = BeautifulSoup(html, "html.parser")
j = soup.find_all("div", class_="search-results")

# with open('savehtml.txt', 'w') as savefile:
for line in j:
    print(line)
#         savefile.write(line)
# savefile.close()
