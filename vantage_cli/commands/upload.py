import os
import sys
import click
from vantage import VantageClient
from printer import Printer, ContentType, Printable
import uuid
from vantage_cli.commands.util import CommandExecutor


def _upload_parquet(
    client,
    collection_id: str,
    content: bytes,
    file_size: int,
    parquet_file_name: str,
) -> str:
    response = client.upload_parquet_embedding(
        collection_id=collection_id,
        content=content,
        file_size=file_size,
        parquet_file_name=parquet_file_name,
    )

    if response == 200:
        return Printable.stdout(
            content="Uploaded successfully.",
            content_type=ContentType.PLAINTEXT,
        )
    else:
        return Printable.stderr(
            content=f"Upload failed with status {response}",
            content_type=ContentType.PLAINTEXT,
        )


def _upload_documents(
    client: VantageClient, collection_id, batch_identifier, documents_file
) -> str:
    response = client.upload_documents_from_jsonl(
        collection_id=collection_id,
        documents=documents_file.read(),
        batch_identifier=batch_identifier,
    )

    if response is None:
        return Printable.stdout(
            content="Uploaded successfully.",
            content_type=ContentType.PLAINTEXT,
        )
    else:
        return Printable.stderr(
            content=f"Upload failed with status {response}",
            content_type=ContentType.PLAINTEXT,
        )


@click.command("upload-parquet")
@click.option(
    "--collection-id",
    type=click.STRING,
    required=True,
    help="Collection ID.",
)
@click.argument(
    "parquet-file",
    required=True,
    type=click.File('rb'),
    default=sys.stdin,
)
@click.pass_obj
def upload_parquet(ctx, collection_id, parquet_file):
    """
    Upload embeddings from Parquet file.

    DOCUMENTS_FILE is a file containing documents in Parquet format.
    It can be passed as a path to a file, or it can be read from stdin.
    """
    # TODO: implement uploading both from file and stdin
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]

    if parquet_file.name == "<stdin>":
        printer.print_text(text="Uploading from stdin...")
        data = parquet_file.buffer.read()
        # Batch identifier MUST have a .parquet suffix,
        # otherwise service won't process it.
        file_name = f"{str(uuid.uuid4())}.parquet"
    else:
        file_name = os.path.basename(parquet_file.name)
        printer.print_text(text=f"Uploading file '{file_name}'...")
        data = parquet_file.read()

    executor.execute_and_print_printable(
        command=lambda: _upload_parquet(
            client=client,
            collection_id=collection_id,
            content=data,
            file_size=len(data),
            parquet_file_name=file_name,
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
    type=click.File('r'),
    default=sys.stdin,
    required=True,
)
@click.pass_obj
def upload_documents(ctx, collection_id, documents_file, batch_identifier):
    """
    Upload embeddings from JSONL file.

    DOCUMENTS_FILE is a file containing documents in JSONL format.
    It can be passed as a path to a file, or it can be read from stdin.
    """
    # TODO: implement uploading both from file and stdin
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]
    printer.print_text(text="Uploading...")

    if batch_identifier is None:
        if documents_file.name == "<stdin>":
            batch_identifier = {str(uuid.uuid4())}
        else:
            batch_identifier = os.path.basename(documents_file.name)

    executor.execute_and_print_printable(
        command=lambda: _upload_documents(
            client=client,
            collection_id=collection_id,
            batch_identifier=batch_identifier,
            documents_file=documents_file,
        ),
        output_type=ContentType.PLAINTEXT,
        printer=printer,
    )
