import urllib.request, requests
import time
from bs4 import BeautifulSoup

url = 'http://taos.com/contact-taos'
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
soup.findAll('a')

one_a_tag = soup.findAll("a")[36]
link = one_a_tag["href"]

for i in range(36,len(soup.findAll('a'))+1):
    one_a_tag = soup.findAll('a')[i]
    link = one_a_tag['href']
    download_url = 'http://taos.com/'+ link
    urllib.request.urlretrieve(download_url)
    time.sleep(1)


def scrape():
    return
