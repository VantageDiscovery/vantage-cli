import click
from vantage_cli.util import get_generic_message_for_exception
from vantage import VantageClient
from vantage.exceptions import VantageNotFoundError
from printer import Printer, Printable, ContentType


@click.command("list-collections")
@click.pass_obj
def list_collections(ctx):
    """Lists existing colections."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    content_type = ContentType.OBJECT

    try:
        content = [item.__dict__ for item in client.list_collections()]
    except Exception as exception:
        content = get_generic_message_for_exception(exception)
        content_type = ContentType.PLAINTEXT

    printer.print(
        Printable(
            content=content,
            content_type=content_type,
        )
    )


@click.command("create-collection")
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
    help="Collecion embedding dimension",
)
@click.option(
    "--llm-provider",
    type=click.STRING,
    required=False,
    help="LLM provider ID (\"OpenAPI\"|\"Hugging\")",
)
@click.option(
    "--external-key-id",
    type=click.STRING,
    required=False,
    help="Key for the external API",
)
@click.option(
    "--collection-preview-url-pattern",
    type=click.STRING,
    required=False,
    help="???",
)
@click.option(
    "--use-provided-embeddings",
    type=click.BOOL,
    required=False,
    help="If the user will upload embeddings to collection afterwards.",
    default=False,
)
@click.pass_obj
def create_collection(
    ctx,
    collection_id,
    collection_name,
    embeddings_dimension,
    llm_provider,
    external_key_id,
    collection_preview_url_pattern,
    use_provided_embeddings,
):
    """Creates a new collection."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    content_type = ContentType.OBJECT

    if llm_provider is None or external_key_id is None:
        llm_provider = None
        external_key_id = None

    try:
        client.create_collection(
            collection_id=collection_id,
            collection_name=collection_name,
            embeddings_dimension=embeddings_dimension,
            user_provided_embeddings=use_provided_embeddings,
            llm=llm_provider,
            external_key_id=external_key_id,
            collection_preview_url_pattern=collection_preview_url_pattern,
        )
    except Exception as exception:
        content = get_generic_message_for_exception(exception)
        content_type = ContentType.PLAINTEXT

    printer.print(
        Printable(
            content=content,
            content_type=content_type,
        )
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

    content_type = ContentType.OBJECT
    try:
        content = client.get_collection(collection_id=collection_id)
    except Exception as exception:
        if isinstance(exception, VantageNotFoundError):
            content = "Collection not found."
        else:
            content = get_generic_message_for_exception(exception)
        content_type = ContentType.PLAINTEXT

    printer.print(
        Printable(
            content=content,
            content_type=content_type,
        )
    )


@click.command("update-collection")
@click.option(
    "--collection-id",
    type=click.STRING,
    required=True,
    help="ID for the new collection.",
)
@click.option(
    "--collection-name",
    type=click.STRING,
    required=False,
    help="Name for the new collection.",
)
@click.option(
    "--external-key-id",
    type=click.STRING,
    required=False,
    help="Key for the external API",
)
@click.option(
    "--collection-preview-url-pattern",
    type=click.STRING,
    required=False,
    help="???",
)
@click.pass_obj
def update_collection(
    ctx,
    collection_id,
    collection_name,
    external_key_id,
    collection_preview_url_pattern,
):
    """Updates collection data."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    content_type = ContentType.OBJECT

    try:
        client.update(
            collection_id=collection_id,
            collection_name=collection_name,
            external_key_id=external_key_id,
            collection_preview_url_pattern=collection_preview_url_pattern,
        )
    except Exception as exception:
        if isinstance(exception, VantageNotFoundError):
            content = "Collection not found."
        else:
            content = get_generic_message_for_exception(exception)
        content_type = ContentType.PLAINTEXT

    printer.print(
        Printable(
            content=content,
            content_type=content_type,
        )
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
    content_type = ContentType.OBJECT

    try:
        content = client.delete_collection(collection_id=collection_id)
    except Exception as exception:
        if isinstance(exception, VantageNotFoundError):
            content = "Collection not found."
        else:
            content = get_generic_message_for_exception(exception)
        content_type = ContentType.PLAINTEXT

    printer.print(
        Printable(
            content=content,
            content_type=content_type,
        )
    )
