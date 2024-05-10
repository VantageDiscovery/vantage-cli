import click
from vantage_sdk import VantageClient
from vantage_cli.printer import Printer, ContentType
from vantage_sdk.core.http.exceptions import NotFoundException
from vantage_cli.commands.util import (
    CommandExecutor,
    specific_exception_handler,
)


@click.command("delete-documents")
@click.argument(
    "collection_id",
    type=click.STRING,
    required=True,
)
@click.option(
    "--document-ids",
    type=click.STRING,
    required=True,
    help="List of document IDs to delete.",
)
@click.pass_obj
def delete_documents(ctx, collection_id: str, document_ids: str):
    """Deletes documents by ID."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]

    executor.execute_and_print_output(
        command=lambda: client.delete_documents(
            collection_id=collection_id,
            document_ids=document_ids,
        ).__dict__,
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=NotFoundException,
            message="Account not found.",
        ),
    )
