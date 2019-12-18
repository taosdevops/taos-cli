from bs4 import BeautifulSoup
from typing import List
from taos import config
import requests
from click import style
import re


search_link = '/about/'
bs4_ignore_strings = [
  "\n", ' ', 'Download Taos Overview >'
]

def _get_next(predicate, object_list):
    return next(obj for obj in object_list if predicate(obj))


def is_leader(tag):
    #return leader h2 tag
    return (tag.name)


def _cleanup(string: str):
    return string.replace("\xa0","")


def get_about():
    """ Returns the content of the taos about page """
    link = "https://taos.com/about/"
    response = requests.get(link, headers={'User-Agent': config.USER_AGENT})
    soup = BeautifulSoup(response.text, "html.parser")

    header = soup.find('h2')
    content = [
        _cleanup(item) for item in header.parent.strings
        if item not in bs4_ignore_strings
    ]

    print("*Run taos about (OPTION) to get specific about pages")
    print("OPTIONS: ")
    from taos import web
    return [*content, *get_leaders()]




def get_leaders():
    def _build_leader(tag):
        try:
            name, title = tag.parent.select('div font')
        except ValueError:
            name = tag.parent.select('div font')[0]
            title = tag.parent.select('div span')[0]
        return {
            "name":name.text,
            "title":title.text
        }

    link = "https://taos.com/about/"
    response = requests.get(link, headers={'User-Agent': config.USER_AGENT})
    soup = BeautifulSoup(response.text, "html.parser")
    link = soup.find(is_leader)
    header = soup.find('h2'=='leadership')

    return [
        f"- {style(leader['title'], bold=True)}: {leader['name']}"
        for leader in [
            _build_leader(item)
            for item in soup.select('div div h4')
        ]
    ]


def list_services():
    url = 'http://taos.com/'
    response = requests.get(url, headers={'User-Agent': config.USER_AGENT})
    soup = BeautifulSoup(response.text, "html.parser")
    services_parent = soup.find(href='/services').parent

    return [
        {"name":"","href":"/about"},
        *[
            {
            "href": tag['href'],
            "name": tag.span.text.strip(re.sub(r'[^\u0000-\u007F]+',' ', str(soup)))
            } for tag in  services_parent.ul.select('li a')
            
        ]
    ]
    

def get_service(service):
    service_record=  _get_next(lambda item: item['name']==service, list_services())
    return _parse_sub(service_record['href'])

def _parse_sub(path:str):
    url = 'http://taos.com'+ path
    response = requests.get(url, headers={'User-Agent': config.USER_AGENT})
    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find('h2')
    title = title_tag.text
    body = title_tag.parent.div.text
    footer = f"\nTo find out more please visit {url}"

    return [title, body, footer]

if __name__ == "__main__":
    pass

