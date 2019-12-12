from bs4 import BeautifulSoup
from typing import List
from taos import config
import requests

search_string = '/taosdevops/dev-ops-now-bios/blob/master/team-members/'
def is_member(tag):
  return (tag.name == 'a') and \
        (tag.has_attr('href') and search_string in tag['href'])

def _get_from_gh():
    url = "https://github.com/taosdevops/dev-ops-now-bios/tree/master/team-members"
    response = requests.get(url, headers={'User-Agent': config.USER_AGENT})
    soup = BeautifulSoup(response.text, "html.parser")
    members = soup.findAll(is_member)
    return [item.string[:-3] for item in members]

def list_persons()-> List[str]:
    return _get_from_gh()

def get_user(user: str)-> dict:
    url = (
        "https://raw.githubusercontent.com/taosdevops/dev-ops-now-bios/"
        f"master/team-members/{user}.md"
    )
    return requests.get(url).content
