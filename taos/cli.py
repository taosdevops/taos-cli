import click
from taos.web import scrape

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
def contact(name, email, service_type):
    print(f"contact, {name}, {email}, {service_type}")
    print(f"<A HREF mailto:contact@taos.com>TEST</A>")


@main.command()
def subscribe():
    print("subscribe")


@main.command()
def bio():
    print("bio")


@main.command()
def subscribe():
    print("subscribe")
