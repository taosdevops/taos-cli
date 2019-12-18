import click
import requests

from taos.web import scrape
from taos.email import send_message
from taos.email import send_message2
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


@click.option("--name", prompt="What is your name?")
@click.option("--email", prompt="What is your Email?")
@click.option(
    "--service-type",
    prompt="which services are you interested in <provide a list of MS PS NOC DON etc>?",
)


@main.command()
def contact(**kwargs):
    print('Taos Contact info:', '888-826-7686','121 Daggett Drive','San Jose, CA 95134')
    req = send_message(**kwargs)
    print(req)


@click.option("--communication", prompt="What is your teams primary form of communication? (Ex: Slack, Managed Services, etc)")
@click.option("--length", prompt="Length of Service?")
@click.option("--hours", prompt="How Many Monthly Hours Are You Interested In?")
@click.option("--service-type", prompt="which services are you interested in <provide a list of MS PS NOC DON etc>?",)
@click.option("--email", prompt="What is your Email?")
@click.option("--name", prompt="What is your name?")


@main.command()
def subscribe(**kwargs):
    req = send_message2(**kwargs)
    print(req)
