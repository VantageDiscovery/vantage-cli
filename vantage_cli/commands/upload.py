import click
from vantage_cli.commands.util import get_generic_message_for_exception
from vantage import VantageClient
from vantage.exceptions import VantageNotFoundError
from printer import Printer


@click.command("upload-parquet")
@click.option(
    "--collection-id",
    type=click.STRING,
    required=True,
    help="Collection ID.",
)
@click.option(
    "--batch-identifier",
    type=click.STRING,
    required=False,
    help="Customer batch identifier.",
)
@click.argument(
    "parquet-file",
    required=True,
    type=click.STRING,
)
@click.pass_obj
def upload_parquet(ctx, collection_id, batch_identifier, parquet_file):
    """Uploads embeddings from .parquet file."""
    # TODO: implement uploading both from file and stdin
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    printer.print_text(text="Uploading...")

    try:
        response = client.upload_embedding_by_path(
            collection_id=collection_id,
            file_path=parquet_file,
            customer_batch_identifier=batch_identifier,
        )
        if response == 200:
            content = "Uploaded successfully."
        else:
            content = f"Upload failed with status {response}"
    except Exception as exception:
        if isinstance(exception, VantageNotFoundError):
            content = "Collection not found."
        else:
            content = get_generic_message_for_exception(exception)

    printer.print_text(text=content)


@click.command("upload-documents")
@click.option(
    "--collection-id",
    type=click.STRING,
    required=True,
    help="Collection ID.",
)
@click.option(
    "--batch-identifier",
    type=click.STRING,
    required=False,
    help="Customer batch identifier.",
)
@click.argument(
    "documents-file",
    type=click.STRING,
    required=True,
)
@click.pass_obj
def upload_documents(ctx, collection_id, documents_file, batch_identifier):
    """Upload embeddings from .jsonl file."""
    # TODO: implement uploading both from file and stdin
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    printer.print_text(text="Uploading...")

    try:
        response = client.upload_embedding_by_path(
            collection_id=collection_id,
            file_path=documents_file,
            customer_batch_identifier=batch_identifier,
        )
        if response == 200:
            content = "Uploaded successfully."
        else:
            content = f"Upload failed with status {response}"
    except Exception as exception:
        if isinstance(exception, VantageNotFoundError):
            content = "Collection not found."
        else:
            content = get_generic_message_for_exception(exception)

    printer.print_text(text=content)
