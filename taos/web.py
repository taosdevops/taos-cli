import urllib.request, requests
import time
from bs4 import BeautifulSoup
from taos import config

bs4_ignore_strings = [
  "\n", ' '
]

url = 'http://taos.com/'
response = requests.get(url, headers={'User-Agent': config.USER_AGENT})
soup = BeautifulSoup(response.text, "html.parser")
is_services = lambda tag: tag.has_attr('href') and tag['href'] == '/services'

services_parent = soup.find(is_services).parent
# print(services_parent.ul) # Service List

services_list = [
  service for service in
  services_parent.ul.strings
  if service and service not in bs4_ignore_strings
]

print(services_list)
