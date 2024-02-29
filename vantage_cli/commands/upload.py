import click
from vantage_cli.util import get_generic_message_for_exception
from vantage import VantageClient
from vantage.exceptions import VantageNotFoundError
from printer import Printer, Printable, ContentType


@click.command("upload-parquet")
@click.option(
    "--collection_id",
    type=click.STRING,
    help="Collection ID.",
)
@click.option(
    "--batch-identifier",
    type=click.STRING,
    help="Customer batch identifier.",
)
@click.option(
    "parquet-file",
    type=click.STRING,
)
@click.pass_obj
def upload_embedding(ctx, collection_id, batch_identifier, parquet_file):
    """Uploads embeddings from .parquet file."""
    # TODO: implement uploading both from file and stdin
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    content_type = ContentType.PLAINTEXT

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

    printer.print(
        Printable(
            content=content,
            content_type=content_type,
        )
    )


@click.command("upload-documents")
@click.option(
    "--collection_id",
    type=click.STRING,
    help="Collection ID.",
)
@click.option(
    "--batch-identifier",
    type=click.STRING,
    help="Customer batch identifier.",
)
@click.option(
    "documents-file",
    type=click.STRING,
)
@click.pass_obj
def upload_documents(ctx, collection_id, documents_file, batch_identifier):
    """Upload embeddings from .jsonl file."""
    # TODO: implement uploading both from file and stdin
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    content_type = ContentType.PLAINTEXT

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

    printer.print(
        Printable(
            content=content,
            content_type=content_type,
        )
    )
