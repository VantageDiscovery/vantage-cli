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


@click.command("create-collection", help="Not Implemented.")
@click.option(
    "--collection-id", type=click.STRING, help="ID for the new collection."
)
@click.option(
    "--collection-name", type=click.STRING, help="Name for the new collection."
)
@click.option(
    "--embedding-dimension",
    type=click.INT,
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
    "--embeddings",
    type=click.STRING,
    required=False,
    help="Path to Parquet file containing embeddings",
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
    embeddings,
):
    """Creates a new collection."""
    click.echo("Not implemented.")
    # client: VantageClient = ctx["client"]
    # printer: Printer = ctx["printer"]

    # if llm_provider is None or external_key_id is None:
    #     llm_provider = None
    #     external_key_id = None

    # try:
    #     client.create_collection(
    #         collection_id=collection_id,
    #         collection_name=collection_name,
    #         embeddings_dimension=embeddings_dimension,
    #         user_provided_embeddings=user_provided_embeddings,
    #         llm=llm_provider,
    #         external_key_id=external_key_id,
    #         collection_preview_url_pattern=collection_preview_url_pattern,
    #     )
    # except Exception as exception:
    #     content = get_generic_message_for_exception(exception)
    #     content_type = ContentType.PLAINTEXT

    # printer.print(
    #     Printable(
    #         content=content,
    #         content_type=content_type,
    #     )
    # )


@click.command("get-collection", help="Not Implemented.")
@click.pass_obj
def get_collection(ctx):
    """Fetches collection details."""
    click.echo("Not implemented.")


@click.command("update-collection", help="Not Implemented.")
@click.pass_obj
def update_collection(ctx):
    """Updates a collection."""
    click.echo("Not implemented.", help="Not Implemented.")


@click.command("delete-collection", help="Not Implemented.")
@click.pass_obj
def delete_collection(ctx):
    """Deletes a collection."""
    click.echo("Not implemented.")
