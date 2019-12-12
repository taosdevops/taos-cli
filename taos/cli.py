import click
import requests
from taos import bio, about
import click 

@click.group()
@click.pass_context
def main(ctx):
    """ Taos cli command """
    pass


@main.command("about")
@click.argument(
    "link", default="",
    # # Commenting out choices till we get a programmatic list of em
    type=click.Choice(about.list_services())
)
def get_about(link):
    """ Looking at Taos Who We Are """

    click.echo(f"{link} Who We Are \n")
    click.echo(about.get_about())
    click.echo()
    click.echo('\n'.join([f"- {leader}" for leader in about.get_leaders()]))


@click.option("--name", prompt="What is your name?")
@click.option("--email", prompt="What is your Email?")
@click.option(
    "--service-type",
    prompt="which services are you interested in <provide a list of MS PS NOC DON etc>?",
)
@main.command()
def contact(name, email, service_type):
    print(f"contact, {name}, {email}, {service_type}")
    print(f"<A HREF mailto:contact@taos.com>TEST</A>")


@main.command()
def subscribe():
    print("subscribe")


@main.command("bio")
@click.argument("user", type=click.Choice(bio.list_persons()))

def bio_get(user):

    """ Lookup Taos personell bio information. """

    click.echo(f"{user} BIO \n")
    click.echo(bio.get_user(user))
