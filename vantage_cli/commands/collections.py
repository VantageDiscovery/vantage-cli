from logging import Logger
import click
from vantage_sdk.client import VantageClient
from vantage_sdk.core.http.exceptions import NotFoundException
from vantage_sdk.model.collection import (
    HuggingFaceCollection,
    OpenAICollection,
    UserProvidedEmbeddingsCollection,
)
from vantage_sdk.model.keys import SecondaryExternalAccount
from vantage_cli.commands.util import (
    specific_exception_handler,
    mask_sensitive_string,
)
from vantage_cli.printer import Printer, ContentType


def _delete_collection(client, collection_id: str) -> str:
    client.delete_collection(collection_id=collection_id)

    return {"id": collection_id}


@click.command("list-collections")
@click.pass_obj
def list_collections(ctx):
    """Lists existing colections."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor = ctx["executor"]
    logger: Logger = ctx["logger"]

    logger.debug("Listing collections...")
    executor.execute_and_print_output(
        command=lambda: [item.__dict__ for item in client.list_collections()],
        output_type=ContentType.OBJECT,
        printer=printer,
    )


@click.command("get-collection")
@click.argument(
    "collection_id",
    type=click.STRING,
    required=True,
)
@click.pass_obj
def get_collection(ctx, collection_id):
    """Fetches collection details."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor = ctx["executor"]
    logger: Logger = ctx["logger"]

    logger.debug(f"Fetching collection with ID {collection_id}")
    executor.execute_and_print_output(
        lambda: client.get_collection(collection_id=collection_id).__dict__,
        ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=NotFoundException,
            message="Collection not found.",
        ),
    )


@click.command("update-collection")
@click.option(
    "--collection-name",
    type=click.STRING,
    required=False,
    help="New name for the collection.",
)
@click.option(
    "--external-key-id",
    type=click.STRING,
    required=False,
    help="New external key ID used in the collection.",
)
@click.option(
    "--collection-preview-url-pattern",
    type=click.STRING,
    required=False,
    help="New URL pattern for previewing items in the collection",
)
@click.argument(
    "collection_id",
    type=click.STRING,
    required=True,
)
@click.pass_obj
def update_collection(
    ctx,
    collection_name,
    external_key_id,
    collection_preview_url_pattern,
    collection_id,
):
    """Updates collection data."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor = ctx["executor"]
    logger: Logger = ctx["logger"]

    data = {
        "collection_id": collection_id,
        "collection_name": collection_name,
        "external_key_id": mask_sensitive_string(external_key_id),
        "collection_preview_url_pattern": collection_preview_url_pattern,
    }
    logger.debug(f"Updating collection with data: {data}")
    executor.execute_and_print_output(
        lambda: client.update_collection(
            collection_id=collection_id,
            collection_name=collection_name,
            external_key_id=external_key_id,
            collection_preview_url_pattern=collection_preview_url_pattern,
        ).__dict__,
        ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=NotFoundException,
            message="Collection not found.",
        ),
    )


@click.command("delete-collection")
@click.argument(
    "collection_id",
    type=click.STRING,
    required=True,
)
@click.pass_obj
def delete_collection(ctx, collection_id):
    """Deletes a collection."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor = ctx["executor"]
    logger: Logger = ctx["logger"]

    logger.debug(f"Deleting collection {collection_id}")
    executor.execute_and_print_output(
        lambda: _delete_collection(client=client, collection_id=collection_id),
        ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=NotFoundException,
            message="Collection not found.",
        ),
    )


@click.command("create-collection-openai")
@click.option(
    "--collection-id",
    type=click.STRING,
    help="ID for the new collection.",
    required=True,
)
@click.option(
    "--collection-name",
    type=click.STRING,
    required=True,
    help="Name for the new collection.",
)
@click.option(
    "--llm-secret",
    type=click.STRING,
    required=True,
    help="OpenAI account secret key.",
)
@click.option(
    "--llm-model-name",
    type=click.STRING,
    required=False,
    default="text-embedding-ada-002",
    help="OpenAI LLM model name.",
)
@click.option(
    "--external-account-id",
    type=click.STRING,
    required=True,
    help="OpenAI account key ID from Vantage Console.",
)
@click.option(
    "--secondary-external-account-id",
    type=click.STRING,
    required=False,
    multiple=True,
    help="Secondary external LLM account key ID.",
)
@click.option(
    "--collection-preview-url-pattern",
    type=click.STRING,
    required=False,
    help="URL pattern for previewing items in the collection.",
)
@click.option(
    "--embeddings-dimension",
    type=click.INT,
    required=False,
    default=1536,
    help="Dimension of the embeddings stored in the collection.",
)
@click.pass_obj
def create_collection_openai(
    ctx,
    collection_id,
    collection_name,
    llm_secret,
    llm_model_name,
    external_account_id,
    secondary_external_account_id,
    collection_preview_url_pattern,
    embeddings_dimension,
):
    """Creates a new OpenAI collection."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor = ctx["executor"]
    logger: Logger = ctx["logger"]

    secondary_external_accounts = [
        SecondaryExternalAccount(
            external_type="OpenAI", external_account_id=ex_id
        )
        for ex_id in secondary_external_account_id
    ]
    data = {
        "collection_id": collection_id,
        "collection_name": collection_name,
        "llm_secret": mask_sensitive_string(llm_secret),
        "llm_model_name": llm_model_name,
        "external_account_id": external_account_id,
        "secondary_external_account_ids": secondary_external_account_id,
        "collection_preview_url_pattern": collection_preview_url_pattern,
        "embeddings_dimension": embeddings_dimension,
    }
    logger.debug(
        "Creating new collection using OpenAI for embeddings with data:"
    )
    logger.debug(data)

    collection = OpenAICollection(
        collection_id=collection_id,
        collection_name=collection_name,
        collection_preview_url_pattern=collection_preview_url_pattern,
        external_account_id=external_account_id,
        secondary_external_accounts=secondary_external_accounts,
        llm_secret=llm_secret,
        llm=llm_model_name,
        embeddings_dimension=embeddings_dimension,
    )

    executor.execute_and_print_output(
        command=lambda: client.create_collection(
            collection=collection
        ).__dict__,
        output_type=ContentType.OBJECT,
        printer=printer,
    )


@click.command("create-collection-hf")
@click.option(
    "--collection-id",
    type=click.STRING,
    help="ID for the new collection.",
    required=True,
)
@click.option(
    "--collection-name",
    type=click.STRING,
    required=True,
    help="Name for the new collection.",
)
@click.option(
    "--llm-secret",
    type=click.STRING,
    required=False,
    help="HuggingFace account secret.",
)
@click.option(
    "--external-account-id",
    type=click.STRING,
    required=False,
    help="HuggingFace account key ID from Vantage Console.",
)
@click.option(
    "--external-url",
    type=click.STRING,
    required=False,
    help="HuggingFace external URL.",
)
@click.option(
    "--collection-preview-url-pattern",
    type=click.STRING,
    required=False,
    help="URL pattern for previewing items in the collection.",
)
@click.option(
    "--embeddings-dimension",
    type=click.INT,
    required=False,
    default=1536,
    help="Dimension of the embeddings stored in the collection.",
)
@click.pass_obj
def create_collection_hf(
    ctx,
    collection_id,
    collection_name,
    llm_secret,
    external_account_id,
    external_url,
    collection_preview_url_pattern,
    embeddings_dimension,
):
    """Creates a new HuggingFace collection."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor = ctx["executor"]
    logger: Logger = ctx["logger"]

    data = {
        "collection_id": collection_id,
        "collection_name": collection_name,
        "llm_secret": mask_sensitive_string(llm_secret),
        "external_url": external_url,
        "external_account_id": external_account_id,
        "collection_preview_url_pattern": collection_preview_url_pattern,
        "embeddings_dimension": embeddings_dimension,
    }
    logger.debug(
        "Creating new collection using HuggingFace for embeddings with data:"
    )
    logger.debug(data)

    collection = HuggingFaceCollection(
        collection_id=collection_id,
        collection_name=collection_name,
        collection_preview_url_pattern=collection_preview_url_pattern,
        external_account_id=external_account_id,
        embeddings_dimension=embeddings_dimension,
        external_url=external_url,
    )

    executor.execute_and_print_output(
        command=lambda: client.create_collection(
            collection=collection
        ).__dict__,
        output_type=ContentType.OBJECT,
        printer=printer,
    )


@click.command("create-collection-upe")
@click.option(
    "--collection-id",
    type=click.STRING,
    help="ID for the new collection.",
    required=True,
)
@click.option(
    "--collection-name",
    type=click.STRING,
    required=True,
    help="Name for the new collection.",
)
@click.option(
    "--embeddings-dimension",
    type=click.INT,
    required=True,
    help="Dimension of the embeddings stored in the collection.",
)
@click.option(
    "--collection-preview-url-pattern",
    type=click.STRING,
    required=False,
    help="URL pattern for previewing items in the collection.",
)
@click.pass_obj
def create_collection_upe(
    ctx,
    collection_id,
    collection_name,
    embeddings_dimension,
    collection_preview_url_pattern,
):
    """Creates a new collection with user provided embeddings."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor = ctx["executor"]
    logger: Logger = ctx["logger"]

    data = {
        "collection_id": collection_id,
        "collection_name": collection_name,
        "collection_preview_url_pattern": collection_preview_url_pattern,
        "embeddings_dimension": embeddings_dimension,
    }
    logger.debug(
        "Creating new collection using user provided embeddings with data:"
    )
    logger.debug(data)

    collection = UserProvidedEmbeddingsCollection(
        collection_id=collection_id,
        embeddings_dimension=embeddings_dimension,
        collection_name=collection_name,
        collection_preview_url_pattern=collection_preview_url_pattern,
    )
    executor.execute_and_print_output(
        command=lambda: client.create_collection(
            collection=collection
        ).__dict__,
        output_type=ContentType.OBJECT,
        printer=printer,
    )
