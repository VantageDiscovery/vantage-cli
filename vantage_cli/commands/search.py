import click
from vantage_cli.util import parse_more_like_these
from vantage import VantageClient
from vantage.exceptions import VantageNotFoundError
from printer import Printer, Printable, ContentType
from commands.util import execute_and_print_output, specific_exception_handler


@click.command("embedding-search")
@click.option(
    "--embedding",
    type=click.STRING,
    required=True,
    help="Embedding used for searching the collection.",
)
@click.option(
    "--collection_id",
    type=click.STRING,
    required=True,
    help="Collection ID.",
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
    help="Search accuracy.",
    required=False,
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

    execute_and_print_output(
        command=lambda: [
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
        ],
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=VantageNotFoundError,
            message="Collection not found.",
        ),
    )


@click.command("semantic-search")
@click.option(
    "--collection_id",
    type=click.STRING,
    required=True,
    help="Collection ID.",
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
    "text",
    type=click.STRING,
    required=True,
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

    execute_and_print_output(
        command=lambda: [
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
        ],
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=VantageNotFoundError,
            message="Collection not found.",
        ),
    )


@click.command("more-like-this-search")
@click.option(
    "--document_id",
    type=click.STRING,
    required=True,
    help="ID of a document in a collection.",
)
@click.option(
    "--request_id",
    type=click.STRING,
    required=True,
    help="Request ID.",
)
@click.option(
    "--collection_id",
    type=click.STRING,
    required=True,
    help="Collection ID.",
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

    execute_and_print_output(
        command=lambda: [
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
        ],
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=VantageNotFoundError,
            message="Collection not found.",
        ),
    )


@click.command("more-like-these-search")
@click.option(
    "--document_id",
    type=click.STRING,
    required=True,
    help="ID of a document in a collection.",
)
@click.option(
    "--request_id",
    type=click.STRING,
    required=True,
    help="Request ID.",
)
@click.option(
    "--collection_id",
    type=click.STRING,
    required=True,
    help="Collection ID.",
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
    "more-like-these",
    type=click.STRING,
    required=True,
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

    execute_and_print_output(
        command=lambda: [
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
        ],
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=VantageNotFoundError,
            message="Collection not found.",
        ),
    )
