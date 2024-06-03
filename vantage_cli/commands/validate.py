from logging import Logger
import sys
from typing import Optional
import click
from vantage_cli.printer import ContentType, Printer
from vantage_cli.commands.util import (
    CommandExecutor,
)
from vantage_sdk.core.validation import VALIDATOR as validator
from vantage_sdk.model.validation import CollectionType


def _get_collection_type(name: str) -> CollectionType:
    if name == CollectionType.USER_PROVIDED_EMBEDDINGS.value.upper:
        return CollectionType.USER_PROVIDED_EMBEDDINGS
    elif CollectionType.OPEN_AI.value.upper:
        return CollectionType.OPEN_AI
    elif CollectionType.HUGGING_FACE.value.upper:
        return CollectionType.HUGGING_FACE

    raise click.BadOptionUsage(f"Invalid collection type: {name}")


def _validate_input_combination(
    collection_type: CollectionType,
    model: Optional[str],
    embeddings_dimension: Optional[int],
):
    if collection_type == CollectionType.USER_PROVIDED_EMBEDDINGS:
        if embeddings_dimension is None:
            raise click.ClickException(
                "Embeddings dimension must be provided when collection type is UPE."
            )


def _validate_jsonl_file(
    jsonl_file: str,
    collection_type_name: str,
    model_name: Optional[str],
    embeddings_dimension: Optional[str],
) -> list[dict]:
    collection_type = _get_collection_type(collection_type_name)
    _validate_input_combination(
        collection_type=collection_type,
        model=model_name,
        embeddings_dimension=embeddings_dimension,
    )
    errors = validator.validate_jsonl(
        file_path=jsonl_file,
        collection_type=collection_type,
        model=model_name,
        embeddings_dimension=embeddings_dimension,
    )

    if any(errors):
        return [error.to_dict() for error in errors]

    return {"message": "OK."}


def _validate_parquet_file(
    parquet_file: str,
    collection_type_name: str,
    model_name: Optional[str],
    embeddings_dimension: Optional[str],
) -> list[dict]:
    collection_type = _get_collection_type(collection_type_name)
    _validate_input_combination(
        collection_type=collection_type,
        model=model_name,
        embeddings_dimension=embeddings_dimension,
    )
    errors = validator.validate_parquet(
        file_path=parquet_file,
        collection_type=collection_type,
        model=model_name,
        embeddings_dimension=embeddings_dimension,
    )

    if any(errors):
        return [error.to_dict() for error in errors]

    return {"message": "OK."}


@click.command("validate-jsonl")
@click.option(
    "--collection-type",
    type=click.Choice(["UPE", "OpenAI", "HuggingFace"], case_sensitive=False),
    required=True,
    help="Collection type for which documents are intended.",
)
@click.option(
    "--model-name",
    type=click.STRING,
    required=False,
    help="Collection ID.",
)
@click.option(
    "--embeddings-dimension",
    type=click.INT,
    required=False,
    help="Collection ID.",
)
@click.argument(
    "jsonl-file",
    type=click.STRING,
    required=True,
)
@click.pass_obj
def validate_jsonl(
    ctx,
    jsonl_file,
    collection_type,
    model_name,
    embeddings_dimension,
):
    """Validates JSONL file."""
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]
    logger: Logger = ctx["logger"]

    logger.debug(f"Validating JSONL file: {jsonl_file}...")
    click.echo("Validating file...")

    executor.execute_and_print_output(
        command=lambda: _validate_jsonl_file(
            jsonl_file=jsonl_file,
            collection_type_name=collection_type,
            model_name=model_name,
            embeddings_dimension=embeddings_dimension,
        ),
        output_type=ContentType.OBJECT,
        printer=printer,
    )


@click.command("validate-parquet")
@click.option(
    "--collection-type",
    type=click.Choice(["UPE", "OpenAI", "HuggingFace"], case_sensitive=False),
    required=True,
    help="Collection type for which documents are intended.",
)
@click.option(
    "--model-name",
    type=click.STRING,
    required=False,
    help="Collection ID.",
)
@click.option(
    "--embeddings-dimension",
    type=click.INT,
    required=False,
    help="Collection ID.",
)
@click.argument(
    "parquet-file",
    type=click.STRING,
    required=True,
)
@click.pass_obj
def validate_parquet(
    ctx,
    parquet_file,
    collection_type,
    model_name,
    embeddings_dimension,
):
    """Validates Parquet file."""
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]
    logger: Logger = ctx["logger"]

    logger.debug(f"Validating Parquet file: {parquet_file}...")
    click.echo("Validating file...")

    executor.execute_and_print_output(
        command=lambda: _validate_parquet_file(
            parquet_file=parquet_file,
            collection_type_name=collection_type,
            model_name=model_name,
            embeddings_dimension=embeddings_dimension,
        ),
        output_type=ContentType.OBJECT,
        printer=printer,
    )
