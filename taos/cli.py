import click


@click.group()
@click.pass_context
def main(ctx):
    """ Taos cli command """
    print("main")


@main.command()
def about():
    print("about")


@main.command()
def contact():
    print("about")


@main.command()
def bio():
    print("bio")


@main.command()
def subscribe():
    print("subscribe")
