from bs4 import BeautifulSoup
from typing import List
from taos import config
import requests



def get_link(link: str):
    url = "https:taos.com/about/"
    return requests.get(link) 