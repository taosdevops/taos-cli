"""
Command Line Interface Module:
    Click powered module provides cli options for taos-cli
"""

import click

from taos import about, bio


@click.group()
@click.pass_context
def main(ctx):
    """ Taos cli command """
    pass


@main.command("about")
@click.argument(
    "link",
    default="",
    type=click.Choice([service["name"] for service in about.list_services()]),
)
def get_about(link):
    """ Looking at Taos Who We Are """
    header, * \
        body = about.get_about(
            bold=True) if not link else about.get_service(link)
    click.echo()
    click.echo(click.style(header, bold=True))
    click.echo()
    click.echo("\n".join(body))
    click.echo()
    click.echo(
        "We also provide a range of services, run taos about SERVICE for more.")
    click.echo("\n".join(about.list_service_names()))


@click.option(
    "--service-type",
    prompt="which services are you interested in <provide a list of MS PS NOC DON etc>?",
)
@click.option("--length", prompt="Length of Service?")
@click.option("--hours", prompt="How Many Monthly Hours Are You Interested In?")
@click.option("--email", prompt="What is your Email?")
@click.option("--name", prompt="What is your name?")
@main.command("subscribe")
def subscribe(name, email, hours, length, communication):
    print(f"subscribe, {name}, {email}, {hours}, {length}, {communication}")


@main.command("contact")
def contact(name, email, service_type):
    click.echo(about.contact_info())
    print(f"contact, {name}, {email}, {service_type}")


@main.command("bio")
@click.argument("user", type=click.Choice(bio.list_persons()))
@click.option(
    "--communication",
    prompt="What is your teams primary form of communication? (Ex: Slack, Managed Services, etc)",
)
def bio_setup(user):
    print(f"bio_setup, {user}")

    """ Lookup Taos personell bio information. """


@main.command("bio")
@click.argument("user", type=click.Choice(bio.list_persons()))
def bio_get(user):
    """ Lookup Taos personell bio information. """
    click.echo(f"{user} BIO \n")
    click.echo(bio.get_user(user))
