"""
Implementation of biography information from Github for DevOps Now members

"""

import requests
from bs4 import BeautifulSoup
from click import style

from taos import config

search_link = "/about/"
bs4_ignore_strings = ["\n", " ", "Download Taos Overview >"]


def _bold(string: str) -> str:
    return style(string, bold=True)


def _get_next(predicate, object_list):
    return next(obj for obj in object_list if predicate(obj))


def is_leader(tag):
    # return leader h2 tag

    return tag.name


def _cleanup(string: str):
    return string.replace("\xa0", "")


def get_about(bold=False):
    """ Returns the content of the taos about page """
    link = "https://taos.com/about/"
    response = requests.get(link, headers={"User-Agent": config.USER_AGENT})
    soup = BeautifulSoup(response.text, "html.parser")

    header = soup.find("h2")
    content = [
        _cleanup(item)

        for item in header.parent.strings

        if item not in bs4_ignore_strings
    ]

    return [*content, *get_leaders(bold=bold)]


def get_leaders(bold=False):
    def _build_leader(tag):
        try:
            name, title = tag.parent.select("div font")
        except ValueError:
            name = tag.parent.select("div font")[0]
            title = tag.parent.select("div span")[0]

        return {"name": name.text, "title": title.text}

    link = "https://taos.com/about/"
    response = requests.get(link, headers={"User-Agent": config.USER_AGENT})
    soup = BeautifulSoup(response.text, "html.parser")
    link = soup.find(is_leader)

    return [
        f"- {_bold(leader['title']) if bold else leader['title']}: {leader['name']}"

        for leader in [_build_leader(item) for item in soup.select("div div h4")]
    ]


def _clean_service_name(name: str) -> str:
    return name.replace("™", "").strip().replace("&", "and").replace(" ", "-").lower()


def list_services():
    url = "http://taos.com/"
    response = requests.get(url, headers={"User-Agent": config.USER_AGENT})
    soup = BeautifulSoup(response.text, "html.parser")
    services_parent = soup.find(href="/services").parent

    return [
        {"name": "", "href": "/about"},
        *[
            {"href": tag["href"], "name": _clean_service_name(tag.span.text)}

            for tag in services_parent.ul.select("li a")
        ],
    ]


def list_service_names():
    return [service["name"] for service in list_services()]


def get_service(service):
    service_record = _get_next(
        lambda item: item["name"] == service, list_services())

    return _parse_sub(service_record["href"])


def _parse_sub(path: str):
    url = "http://taos.com" + path
    response = requests.get(url, headers={"User-Agent": config.USER_AGENT})
    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("h2")
    title = title_tag.text
    body = title_tag.parent.div.text
    footer = f"\nTo find out more please visit {url}"

    return [title, body, footer]


def contact_info():
    return " 'Contact info': 'Phone: '888-826-7686', 'contactus@taos.com', '121 Daggett Drive','San Jose, CA 95134'"
