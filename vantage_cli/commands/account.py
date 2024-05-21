from logging import Logger
import click
from vantage_cli.printer import ContentType
from vantage_sdk.client import VantageClient
from vantage_sdk.core.http.exceptions import NotFoundException
from vantage_cli.commands.util import specific_exception_handler


@click.command("get-account")
@click.pass_obj
def get_account(ctx):
    """Fetches Vantage account details."""
    client: VantageClient = ctx["client"]
    printer = ctx["printer"]
    executor = ctx["executor"]
    logger: Logger = ctx["logger"]

    logger.debug("Getting account details...")

    executor.execute_and_print_output(
        command=lambda: client.get_account().__dict__,
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=NotFoundException,
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
    client: VantageClient = ctx["client"]
    printer = ctx["printer"]
    executor = ctx["executor"]
    logger: Logger = ctx["logger"]

    logger.debug(f"Updating account with name: {new_account_name}")

    executor.execute_and_print_output(
        command=lambda: client.update_account(
            account_name=new_account_name
        ).__dict__,
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=NotFoundException,
            message="Account not found.",
        ),
    )
