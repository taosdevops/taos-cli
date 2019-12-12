from bs4 import BeautifulSoup
from typing import List
from taos import config
import requests

search_link = '/about/'
bs4_ignore_strings = [
  "\n", ' ', 'Download Taos Overview >'
]


def is_link(tag):
    return (tag.name == 'a') and \
            (tag.has_attr('href') and search_link in tag['href'])

def is_leader(tag):
    #return leader h2 tag
    return (tag.name)

def is_title(tag):
    if tag.name != 'h2': return False
    return (tag.name == 'h2') and \
            (tag.has_attr('class'))

def _cleanup(string: str):
    return string.replace("\xa0","")

def get_about():
    """ Returns the content of the taos about page """
    link = "https://taos.com/about/"
    response = requests.get(link, headers={'User-Agent': config.USER_AGENT})
    soup = BeautifulSoup(response.text, "html.parser")
    link = soup.find(is_link)

    header = soup.find('h2')
    content = [
        _cleanup(item) for item in header.parent.strings
        if item not in bs4_ignore_strings
    ]

    return "\n".join(content)

def get_leaders():

    # get h2 leader tag and the names/titles below

    link = "https://taos.com/about/"
    response = requests.get(link, headers={'User-Agent': config.USER_AGENT})
    soup = BeautifulSoup(response.text, "html.parser")
    

    return [
        "LEADER1","LEADER2","LEADER3"
    ]


def get_about_2():
    """ Returns the content of the taos about page """
    link = "https://taos.com/about/"
    response = requests.get(link, headers={'User-Agent': config.USER_AGENT})
    soup = BeautifulSoup(response.text, "html.parser")
    link = soup.find(is_link)

    header = soup.find('h2')
    header_content = "".join([item for item in header.parent.strings])
    print(header.parent.div)
    body_content = "".join([item for item in header.parent.div.strings])
    return "\n".join([
        header_content, body_content
    ])

def list_services():    
    url = 'http://taos.com/'
    response = requests.get(url, headers={'User-Agent': config.USER_AGENT})
    soup = BeautifulSoup(response.text, "html.parser")
    is_services = lambda tag: tag.has_attr('href') and tag['href'] == '/services'

    services_parent = soup.find(is_services).parent

    return ["", *[
        service for service in
        services_parent.ul.strings
        if service and service not in bs4_ignore_strings
    ]]


if __name__ == "__main__":
    print(
        get_about_2()
    )
