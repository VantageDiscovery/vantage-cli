from logging import Logger
import os
import sys
import click
from vantage_sdk import VantageClient
from vantage_sdk.core.http.exceptions import NotFoundException
from vantage_cli.printer import Printer, ContentType
import uuid
from vantage_cli.commands.util import (
    CommandExecutor,
    specific_exception_handler,
)


def _upsert_parquet(
    client: VantageClient,
    collection_id: str,
    parquet_file_name: str,
) -> str:
    response = client.upsert_documents_from_parquet_file(
        collection_id=collection_id,
        parquet_file_path=parquet_file_name,
    )

    if response == 200:
        message = "Successfully sent to processing."
    else:
        message = f"Processing failed with status {response}"

    return {"response": message}


def _upsert_jsonl(
    client: VantageClient,
    collection_id: str,
    batch_identifier: str,
    documents_file,
) -> str:
    response = client.upsert_documents_from_jsonl_string(
        collection_id=collection_id,
        documents_jsonl=documents_file.read(),
        batch_identifier=batch_identifier,
    )

    if response is None:
        message = "Successfully sent to processing."
    else:
        message = f"Sending to processing failed with status {response}"

    return {"response": message}


@click.command("upsert-documents-from-parquet")
@click.option(
    "--collection-id",
    type=click.STRING,
    required=True,
    help="Collection ID.",
)
@click.argument(
    "parquet-file",
    required=True,
    type=click.STRING,
)
@click.pass_obj
def upsert_documents_from_parquet(ctx, collection_id, parquet_file):
    """
    Upserts documents from a Parquet file.

    DOCUMENTS_FILE is a file containing documents in Parquet format.
    It can be passed as a path to a file, or it can be read from stdin.
    """
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]
    logger: Logger = ctx["logger"]

    logger.debug(f"Upserting documents from Parquet file: {parquet_file}")

    # NOTE: Batch identifier MUST have a ".parquet" suffix,
    # otherwise service won't process it.
    if not parquet_file.endswith(".parquet"):
        printer.stderr("File must have .parquet extension.")
        sys.exit(1)

    printer.print_text(text=f"Uploading file '{parquet_file}'...")

    executor.execute_and_print_output(
        command=lambda: _upsert_parquet(
            client=client,
            collection_id=collection_id,
            parquet_file_name=parquet_file,
        ),
        output_type=ContentType.OBJECT,
        printer=printer,
    )


@click.command("upsert-documents-from-jsonl")
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
def upsert_documents_from_jsonl(
    ctx,
    collection_id,
    documents_file,
    batch_identifier,
):
    """
    Upserts documents from a JSONL file.

    DOCUMENTS_FILE is a file containing documents in JSONL format.
    It can be passed as a path to a file, or it can be read from stdin.
    """
    # TODO: implement uploading both from file and stdin
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]
    logger: Logger = ctx["logger"]

    logger.debug(f"Upserting documents from JSONL file: {documents_file}")
    printer.print_text(text="Uploading...")

    if batch_identifier is None:
        if documents_file.name == "<stdin>":
            batch_identifier = {str(uuid.uuid4())}
        else:
            batch_identifier = os.path.basename(documents_file.name)
    logger.debug(f"Batch identifier set to {batch_identifier}")

    executor.execute_and_print_output(
        command=lambda: _upsert_jsonl(
            client=client,
            collection_id=collection_id,
            batch_identifier=batch_identifier,
            documents_file=documents_file,
        ),
        output_type=ContentType.OBJECT,
        printer=printer,
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
    help="IDs of documents to delete, separated by a comma. For example: \"1, 2, 3, 4, 5\".",
)
@click.pass_obj
def delete_documents(ctx, collection_id: str, document_ids: str):
    """Deletes documents by ID."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]
    logger: Logger = ctx["logger"]

    logger.debug(f"Deleting documents with IDs: {document_ids}")
    executor.execute_and_print_output(
        command=lambda: client.delete_documents(
            collection_id=collection_id,
            document_ids=document_ids.split(","),
        ).__dict__,
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=NotFoundException,
            message="Account not found.",
        ),
    )
