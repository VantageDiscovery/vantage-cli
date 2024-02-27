import click
from printer import Printable, ContentType


@click.command("get-account")
@click.pass_obj
def get_account(ctx):
    """Fetches Vantage account details."""
    client = ctx["client"]
    printer = ctx["printer"]

    response = Printable(
        content=client.get_account().__dict__,
        content_type=ContentType.OBJECT,
    )
    printer.print(response)


@click.command("update-account")
@click.argument("name", type=click.STRING)
@click.pass_obj
def update_account(ctx, name):
    """Updates details of a vantage account.

    name: Vantage account name.
    """
    client = ctx["client"]
    printer = ctx["printer"]

    response = Printable(
        client.update_account(account_name=name).__dict__,
        content_type=ContentType.OBJECT,
    )
    printer.print(response)
