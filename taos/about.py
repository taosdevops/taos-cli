from bs4 import BeautifulSoup
from typing import List
from taos import config
import requests



def get_link(url: str):
    url = "https://taos.com/about/"
    return requests.get(url)

def get_about():
    """ Returns the content of the taos about page """
    url = "https://taos.com/about/whoweare"
    response = requests.get(url, headers={'User-Agent': config.USER_AGENT})
    soup = BeautifulSoup(response.text, "html.parser")
    return soup(url)

    