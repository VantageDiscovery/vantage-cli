import click
from printer import ContentType
from vantage.exceptions import VantageNotFoundError
from commands.util import execute_and_print_output, specific_exception_handler


@click.command("get-account")
@click.pass_obj
def get_account(ctx):
    """Fetches Vantage account details."""
    client = ctx["client"]
    printer = ctx["printer"]

    execute_and_print_output(
        command=lambda: client.get_account().__dict__,
        output_type=ContentType.OBJECT,
        printer=printer,
    )


@click.command("update-account")
@click.argument(
    "name",
    type=click.STRING,
    required=True,
)
@click.pass_obj
def update_account(ctx, name):
    """Updates details of a vantage account."""
    client = ctx["client"]
    printer = ctx["printer"]

    execute_and_print_output(
        command=lambda: client.update_account(account_name=name).__dict__,
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=VantageNotFoundError,
            message="Account not found.",
        ),
    )
