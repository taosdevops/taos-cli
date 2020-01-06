import click
import requests

from taos.email import send_message, send_message2
from taos import about, bio, config


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


@click.option(
    "--service-type",
    prompt="which services are you interested in <provide a list of MS PS NOC DON etc>?",
)
@click.option("--email", prompt="What is your Email?")
@click.option("--name", prompt="What is your name?")
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
    if req:
        print("Thanks for contacting taos!")
        return
    print(
        "It looks like there was an issue submitting the email, please "
        "check that the environment variable SEND_GRID_API_KEY is set. "
        "You can also visit https://www.taos.com/contact-taos to submit a request online."
    )


@main.command("bio")
@click.argument("user", type=click.Choice(bio.list_persons()))
def bio_get(user):
    """ Lookup Taos personell bio information. """
    click.echo(f"{user} BIO \n")
    click.echo(bio.get_user(user))

if __name__ == '__main__':
    subscribe()#**{
        # "communication":"slack",
        # "length":"2mo",
        # "hours":"80",
        # "service-type":"dons",
        # "email":"amcchesney@taos.com",
        # "name":"adam mcchesney",})
