import click
from vantage_cli.printer import ContentType
from vantage.exceptions import VantageNotFoundError
from vantage_cli.commands.util import specific_exception_handler


@click.command("get-account")
@click.pass_obj
def get_account(ctx):
    """Fetches Vantage account details."""
    client = ctx["client"]
    printer = ctx["printer"]
    executor = ctx["executor"]

    executor.execute_and_print_output(
        command=lambda: client.get_account().__dict__,
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=VantageNotFoundError,
            message="Account not found.",
        ),
    )


@click.command("update-account")
@click.argument(
    "new_account_name",
    type=click.STRING,
    required=True,
)
@click.pass_obj
def update_account(ctx, new_account_name):
    """Updates details of a Vantage account."""
    client = ctx["client"]
    printer = ctx["printer"]
    executor = ctx["executor"]

    executor.execute_and_print_output(
        command=lambda: client.update_account(
            account_name=new_account_name
        ).__dict__,
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=VantageNotFoundError,
            message="Account not found.",
        ),
    )
