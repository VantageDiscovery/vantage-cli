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


@click.command("create-collection")
@click.option("--collection-id", type=click.STRING)
@click.option("--collection-name", type=click.STRING)
@click.option("--embedding-dimension", type=click.INT)
@click.option("--llm-provider", type=click.STRING, required=False)
@click.option("--external-key-id", type=click.STRING, required=False)
@click.option(
    "--collection-preview-url-pattern", type=click.STRING, required=False
)
@click.option("--embeddings", type=click.STRING, required=False)
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
    """
    Creates a new collection.

    usage:
        create-collection [OPTIONS]

    options:
        --collection-id                  : ID for the new collection.
        --collection-name                : Name for the new collection.
        --embedding-dimension            : Collecion embedding dimension
        --llm-provider                   : LLM provider ID ("OpenAPI"|"Hugging")
        --external-key-id                : Key for the external API
        --collection-preview-url-pattern : ???
        --embeddings                     : Path to Parquet file containing embeddings
    """
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


@click.command("get-collection")
@click.pass_obj
def get_collection(ctx):
    """Fetches collection details."""
    click.echo("Not implemented.")


@click.command("update-collection")
@click.pass_obj
def update_collection(ctx):
    """Updates a collection."""
    click.echo("Not implemented.")


@click.command("delete-collection")
@click.pass_obj
def delete_collection(ctx):
    """Deletes a collection."""
    click.echo("Not implemented.")
