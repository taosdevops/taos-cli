import click
import requests

from taos.web import scrape
from taos.email import send_message
from taos import config

def _is_status_ok(request):
    return request.status_code >= 200 and \
            request.status_code < 300 and \
            request.headers.get("X-Frame-Options") != "DENY"

@click.group()
@click.pass_context
def main(ctx):
    """ Taos cli command """
    pass


@main.command()
def about():
    print("about")
    scrape("urls")


@click.option("--name", prompt="What is your name?")
@click.option("--email", prompt="What is your Email?")
@click.option(
    "--service-type",
    prompt="which services are you interested in <provide a list of MS PS NOC DON etc>?",
)
@main.command()
def contact(**kwargs):
    req = requests.post(f"https://{config.CONTACT_ENDPOINT}", json=kwargs)
    print(req)
    if not _is_status_ok(req):
        print(f"Error sending email, please visit {config.CONTACT_WEB_SITE}")
        exit(0)
    print("Information succesfully sent.")


@main.command()
def subscribe():
    print("subscribe")


@main.command()
def bio():
    print("bio")


@main.command()
def subscribe():
    print("subscribe")
