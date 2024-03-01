import click
from vantage import VantageClient
from printer import Printer, ContentType


def _upload_parquet(
    client, collection_id, batch_identifier, parquet_file
) -> str:
    response = client.upload_embedding_by_path(
        collection_id=collection_id,
        file_path=parquet_file,
        customer_batch_identifier=batch_identifier,
    )
    if response == 200:
        content = "Uploaded successfully."
    else:
        content = f"Upload failed with status {response}"

    return content


def _upload_documents(
    client, collection_id, batch_identifier, documents_file
) -> str:
    response = client.upload_embedding_by_path(
        collection_id=collection_id,
        file_path=documents_file,
        customer_batch_identifier=batch_identifier,
    )
    if response == 200:
        content = "Uploaded successfully."
    else:
        content = f"Upload failed with status {response}"

    return content


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
    executor = ctx["executor"]
    printer.print_text(text="Uploading...")

    executor.execute_and_print_output(
        command=lambda: _upload_parquet(
            client=client,
            collection_id=collection_id,
            batch_identifier=batch_identifier,
            parquet_file=parquet_file,
        ),
        output_type=ContentType.PLAINTEXT,
        printer=printer,
    )


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
    executor = ctx["executor"]
    printer.print_text(text="Uploading...")

    executor.execute_and_print_output(
        command=lambda: _upload_documents(
            client=client,
            collection_id=collection_id,
            batch_identifier=batch_identifier,
            documents_file=documents_file,
        ),
        output_type=ContentType.PLAINTEXT,
        printer=printer,
    )
