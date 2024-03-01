import click
from vantage_cli.util import (
    get_generic_message_for_exception,
    parse_more_like_these,
)
from vantage import VantageClient
from vantage.exceptions import VantageNotFoundError
from printer import Printer, Printable, ContentType


@click.command("embedding-search")
@click.option(
    "--embedding",
    type=click.STRING,
    help="Embedding used for searching the collection.",
)
@click.option(
    "--collection_id",
    type=click.STRING,
    help="Collection ID.",
)
@click.option(
    "--vantage-api-key",
    type=click.STRING,
    help="Vantage API key used for search.",
)
@click.option(
    "--accuracy",
    type=click.FLOAT,
    help="Search accuracy.",
    required=False,
)
@click.option(
    "--page",
    type=click.INT,
    help="Search page.",
    required=False,
)
@click.option(
    "--items-per-page",
    type=click.INT,
    help="Items returned per search page.",
    required=False,
)
@click.option(
    "--boolean-filter",
    type=click.STRING,
    help="Search filter.",
    required=False,
)
@click.pass_obj
def embedding_search(
    ctx,
    embedding,
    collection_id,
    accuracy,
    page,
    items_per_page,
    boolean_filter,
    vantage_api_key,
):
    """Search using provided embeddings."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    content_type = ContentType.OBJECT

    try:
        content = [
            item.__dict__
            for item in client.embedding_search(
                embedding=embedding,
                collection_id=collection_id,
                accuracy=accuracy,
                page=page,
                page_count=items_per_page,
                boolean_filter=boolean_filter,
                vantage_api_key=vantage_api_key,
            ).results
        ]
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


@click.command("semantic-search")
@click.option(
    "--collection_id",
    type=click.STRING,
    help="Collection ID.",
)
@click.option(
    "--vantage-api-key",
    type=click.STRING,
    help="Vantage API key used for search.",
)
@click.option(
    "--accuracy",
    type=click.FLOAT,
    help="Search accuracy.",
    required=False,
)
@click.option(
    "--page",
    type=click.INT,
    help="Search page.",
    required=False,
)
@click.option(
    "--items-per-page",
    type=click.INT,
    help="Items returned per search page.",
    required=False,
)
@click.option(
    "--boolean-filter",
    type=click.STRING,
    help="Search filter.",
    required=False,
)
@click.argument(
    "text",
    type=click.STRING,
)
@click.pass_obj
def semantic_search(
    ctx,
    collection_id,
    accuracy,
    page,
    items_per_page,
    boolean_filter,
    vantage_api_key,
    text,
):
    """Search using text."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    content_type = ContentType.OBJECT

    try:
        content = [
            item.__dict__
            for item in client.embedding_search(
                text=text,
                collection_id=collection_id,
                accuracy=accuracy,
                page=page,
                page_count=items_per_page,
                boolean_filter=boolean_filter,
                vantage_api_key=vantage_api_key,
            ).results
        ]
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


@click.command("more-like-this-search")
@click.option(
    "--document_id",
    type=click.STRING,
    help="ID of a document in a collection.",
)
@click.option(
    "--request_id",
    type=click.STRING,
    help="Request ID.",
)
@click.option(
    "--collection_id",
    type=click.STRING,
    help="Collection ID.",
)
@click.option(
    "--vantage-api-key",
    type=click.STRING,
    help="Vantage API key used for search.",
)
@click.option(
    "--accuracy",
    type=click.FLOAT,
    help="Search accuracy.",
    required=False,
)
@click.option(
    "--page",
    type=click.INT,
    help="Search page.",
    required=False,
)
@click.option(
    "--items-per-page",
    type=click.INT,
    help="Items returned per search page.",
    required=False,
)
@click.option(
    "--boolean-filter",
    type=click.STRING,
    help="Search filter.",
    required=False,
)
@click.pass_obj
def more_like_this_search(
    ctx,
    document_id,
    request_id,
    collection_id,
    accuracy,
    page,
    items_per_page,
    boolean_filter,
    vantage_api_key,
):
    """Finds more like this."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    content_type = ContentType.OBJECT

    try:
        content = [
            item.__dict__
            for item in client.more_like_this_search(
                accuracy=accuracy,
                document_id=document_id,
                collection_id=collection_id,
                page=page,
                page_count=items_per_page,
                request_id=request_id,
                boolean_filter=boolean_filter,
                vantage_api_key=vantage_api_key,
            ).results
        ]
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


@click.command("more-like-these-search")
@click.option(
    "--document_id",
    type=click.STRING,
    help="ID of a document in a collection.",
)
@click.option(
    "--request_id",
    type=click.STRING,
    help="Request ID.",
)
@click.option(
    "--collection_id",
    type=click.STRING,
    help="Collection ID.",
)
@click.option(
    "--vantage-api-key",
    type=click.STRING,
    help="Vantage API key used for search.",
)
@click.option(
    "--accuracy",
    type=click.FLOAT,
    help="Search accuracy.",
    required=False,
)
@click.option(
    "--page",
    type=click.INT,
    help="Search page.",
    required=False,
)
@click.option(
    "--items-per-page",
    type=click.INT,
    help="Items returned per search page.",
    required=False,
)
@click.option(
    "--boolean-filter",
    type=click.STRING,
    help="Search filter.",
    required=False,
)
@click.argument(
    "more-like-these",
    type=click.STRING,
)
@click.pass_obj
def more_like_these_search(
    ctx,
    document_id,
    request_id,
    collection_id,
    accuracy,
    page,
    items_per_page,
    boolean_filter,
    vantage_api_key,
    more_like_these,
):
    """Finds more like these."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    content_type = ContentType.OBJECT

    try:
        more_like_these = parse_more_like_these(more_like_these)
    except Exception:
        printer.print(
            Printable(
                content="Invalid JSON input",
                content_type=ContentType.PLAINTEXT,
            )
        )
        return

    try:
        content = [
            item.__dict__
            for item in client.more_like_these_search(
                accuracy=accuracy,
                document_id=document_id,
                collection_id=collection_id,
                page=page,
                page_count=items_per_page,
                request_id=request_id,
                boolean_filter=boolean_filter,
                vantage_api_key=vantage_api_key,
                more_like_these=more_like_these,
            ).results
        ]
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
