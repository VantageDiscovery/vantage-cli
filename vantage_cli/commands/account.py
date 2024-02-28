import click
from printer import Printable, ContentType
from vantage_cli.util import get_generic_message_for_exception
from vantage.exceptions import VantageNotFoundError


@click.command("get-account")
@click.pass_obj
def get_account(ctx):
    """Fetches Vantage account details."""
    client = ctx["client"]
    printer = ctx["printer"]

    content_type = ContentType.OBJECT
    try:
        content = client.get_account().__dict__
    except Exception as exception:
        if isinstance(exception, VantageNotFoundError):
            content = "User not found."
        else:
            content = get_generic_message_for_exception(exception)
        content_type = ContentType.PLAINTEXT

    printer.print(
        Printable(
            content=content,
            content_type=content_type,
        )
    )


@click.command("update-account")
@click.argument("name", type=click.STRING)
@click.pass_obj
def update_account(ctx, name):
    """
    Updates details of a vantage account.

    usage:
        update-account <name>

    arguments:
        name: Vantage account name.
    """
    client = ctx["client"]
    printer = ctx["printer"]

    try:
        content = client.update_account(account_name=name).__dict__
    except Exception as exception:
        if isinstance(exception, VantageNotFoundError):
            content = "User not found."
        else:
            content = get_generic_message_for_exception(exception)
        content_type = ContentType.PLAINTEXT

    printer.print(
        Printable(
            content=content,
            content_type=content_type,
        )
    )
