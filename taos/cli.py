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
    type=click.Choice([service['name'] for service in about.list_services()])
)
def get_about(link):
    """ Looking at Taos Who We Are """
    header, *body = about.get_about() if not link else about.get_service(link)
    click.echo()
    click.echo(click.style(header, bold=True))
    click.echo()
    click.echo('\n'.join(body))

click.echo(about.contact_info()) 
@click.option("--name", prompt="What is your name?")
@click.option("--email", prompt="What is your Email?")
@click.option(
    "--service-type",
    prompt="which services are you interested in <provide a list of MS PS NOC DON etc>?",
)
@main.command()
def contact(name, email, service_type):
    print(f"contact, {name}, {email}, {service_type}")
    print(f"<A HREF mailto:cmorrow@taos.com>TEST</A>")
    
   

@main.command()
def subscribe():
    print("subscribe")


@main.command("bio")
@click.argument("user", type=click.Choice(bio.list_persons()))

def bio_get(user):

    """ Lookup Taos personell bio information. """

    click.echo(f"{user} BIO \n")
    click.echo(bio.get_user(user))