import click
import requests
from taos.web import scrape
from taos import bio

@click.group()
@click.pass_context
def main(ctx):
    pass


@main.command()
def about():
    """ Print information about Taos """
    print("about")
    scrape("urls")


@click.option("--name", prompt="What is your name?", help="Name submitted to taos contacts.")
@click.option("--email", prompt="What is your Email?", help="Email submitted to taos contacts.")
@click.option(
    "--service-type",
    prompt="which services are you interested in <provide a list of MS PS NOC DON etc>?",
    help="Type of support services that you are interested in."
)
@main.command()
def contact(name, email, service_type):
    """ Send a contact request to taos """
    print(f"contact, {name}, {email}, {service_type}")
    print(f"<A HREF mailto:contact@taos.com>TEST</A>")


@main.command()
def subscribe():
    """ Send a service subscription request to taos """
    print("subscribe")


@main.command("bio")
@click.argument("user", type=click.Choice(bio.list_persons()))
def bio_get(user):
    """ Lookup Taos personell bio information. """
    click.echo(f"{user} BIO \n")
    click.echo(bio.get_user(user))
