import sys
import click
import jsonpickle
from vantage_cli.commands.util import parse_more_like_these
from vantage import VantageClient
from vantage.exceptions import VantageNotFoundError
from vantage_cli.printer import Printer, Printable, ContentType
from vantage_cli.commands.util import (
    specific_exception_handler,
    CommandExecutor,
)


# Used to pass API key from configuration.
COMMAND_NAMES = [
    "search-embedding",
    "search-semantic",
    "search-more-like-this",
    "search-more-like-these",
]


@click.command("search-embedding")
@click.option(
    "--embedding",
    type=click.STRING,
    required=True,
    help="Embedding query vector.",
)
@click.option(
    "--vantage-api-key",
    type=click.STRING,
    required=True,
    help="Vantage API key used for search.",
)
@click.option(
    "--accuracy",
    type=click.FLOAT,
    required=False,
    help="Search accuracy.",
)
@click.option(
    "--page",
    type=click.INT,
    required=False,
    help="Search page.",
)
@click.option(
    "--items-per-page",
    type=click.INT,
    required=False,
    help="Items returned per search page.",
)
@click.option(
    "--boolean-filter",
    type=click.STRING,
    required=False,
    help="Search filter.",
)
@click.argument(
    "collection_id",
    type=click.STRING,
    required=True,
)
@click.pass_obj
def embedding_search(
    ctx,
    embedding,
    accuracy,
    page,
    items_per_page,
    boolean_filter,
    vantage_api_key,
    collection_id,
):
    """Search based on the provided embedding vector."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]

    executor.execute_and_print_output(
        command=lambda: [
            item.__dict__
            for item in client.embedding_search(
                embedding=jsonpickle.loads(embedding),
                collection_id=collection_id,
                accuracy=accuracy,
                page=page,
                page_count=items_per_page,
                boolean_filter=boolean_filter,
                vantage_api_key=vantage_api_key,
            ).results
        ],
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=VantageNotFoundError,
            message="Collection not found.",
        ),
    )


@click.command("search-semantic")
@click.option(
    "--text",
    type=click.STRING,
    required=True,
    help="Text query.",
)
@click.option(
    "--vantage-api-key",
    type=click.STRING,
    required=True,
    help="Vantage API key used for search.",
)
@click.option(
    "--accuracy",
    type=click.FLOAT,
    required=False,
    help="Search accuracy.",
)
@click.option(
    "--page",
    type=click.INT,
    required=False,
    help="Search page.",
)
@click.option(
    "--items-per-page",
    type=click.INT,
    required=False,
    help="Items returned per search page.",
)
@click.option(
    "--boolean-filter",
    type=click.STRING,
    required=False,
    help="Search filter.",
)
@click.argument(
    "collection_id",
    type=click.STRING,
    required=True,
)
@click.pass_obj
def semantic_search(
    ctx,
    text,
    accuracy,
    page,
    items_per_page,
    boolean_filter,
    vantage_api_key,
    collection_id,
):
    """Search based on the provided text query."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]

    executor.execute_and_print_output(
        command=lambda: [
            item.__dict__
            for item in client.semantic_search(
                text=text,
                collection_id=collection_id,
                accuracy=accuracy,
                page=page,
                page_count=items_per_page,
                boolean_filter=boolean_filter,
                vantage_api_key=vantage_api_key,
            ).results
        ],
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=VantageNotFoundError,
            message="Collection not found.",
        ),
    )


@click.command("search-more-like-this")
@click.option(
    "--document_id",
    type=click.STRING,
    required=True,
    help="ID of a document in a collection.",
)
@click.option(
    "--vantage-api-key",
    type=click.STRING,
    required=True,
    help="Vantage API key used for search.",
)
@click.option(
    "--accuracy",
    type=click.FLOAT,
    required=False,
    help="Search accuracy.",
)
@click.option(
    "--page",
    type=click.INT,
    required=False,
    help="Search page.",
)
@click.option(
    "--items-per-page",
    type=click.INT,
    required=False,
    help="Items returned per search page.",
)
@click.option(
    "--boolean-filter",
    type=click.STRING,
    required=False,
    help="Search filter.",
)
@click.argument(
    "collection_id",
    type=click.STRING,
    required=True,
)
@click.pass_obj
def more_like_this_search(
    ctx,
    document_id,
    accuracy,
    page,
    items_per_page,
    boolean_filter,
    vantage_api_key,
    collection_id,
):
    """Search based on the provided document ID."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]

    executor.execute_and_print_output(
        command=lambda: [
            item.__dict__
            for item in client.more_like_this_search(
                accuracy=accuracy,
                document_id=document_id,
                collection_id=collection_id,
                page=page,
                page_count=items_per_page,
                boolean_filter=boolean_filter,
                vantage_api_key=vantage_api_key,
            ).results
        ],
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=VantageNotFoundError,
            message="Collection not found.",
        ),
    )


@click.command("search-more-like-these")
@click.option(
    "--more-like-these-json",
    type=click.File('r'),
    default=sys.stdin,
    required=True,
    help="Path to the JSON file containing a list of `these` objects.",
)
@click.option(
    "--vantage-api-key",
    type=click.STRING,
    required=True,
    help="Vantage API key used for search.",
)
@click.option(
    "--accuracy",
    type=click.FLOAT,
    required=False,
    help="Search accuracy.",
)
@click.option(
    "--page",
    type=click.INT,
    required=False,
    help="Search page.",
)
@click.option(
    "--items-per-page",
    type=click.INT,
    required=False,
    help="Items returned per search page.",
)
@click.option(
    "--boolean-filter",
    type=click.STRING,
    required=False,
    help="Search filter.",
)
@click.argument(
    "collection_id",
    type=click.STRING,
    required=True,
)
@click.pass_obj
def more_like_these_search(
    ctx,
    more_like_these_json,
    accuracy,
    page,
    items_per_page,
    boolean_filter,
    vantage_api_key,
    collection_id,
):
    """
    Search based on the provided MoreLikeThese items.
    """
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]

    try:
        more_like_these = parse_more_like_these(more_like_these_json.read())
    except Exception:
        printer.print(
            Printable.stderr(
                content="Invalid JSON input",
                content_type=ContentType.PLAINTEXT,
            )
        )
        return

    executor.execute_and_print_output(
        command=lambda: [
            item.__dict__
            for item in client.more_like_these_search(
                accuracy=accuracy,
                collection_id=collection_id,
                page=page,
                page_count=items_per_page,
                boolean_filter=boolean_filter,
                vantage_api_key=vantage_api_key,
                more_like_these=more_like_these,
            ).results
        ],
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=VantageNotFoundError,
            message="Collection not found.",
        ),
    )
