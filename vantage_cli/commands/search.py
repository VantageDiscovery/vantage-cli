import traceback
from logging import Logger
import sys
from typing import List, Optional
import click
import jsonpickle
from vantage_cli.commands.util import parse_more_like_these
from vantage_sdk.client import VantageClient
from vantage_sdk.core.http.exceptions import NotFoundException
from vantage_sdk.model.search import (
    Pagination,
    FieldValueWeighting,
    WeightedFieldValueItem,
    Sort,
    Filter,
)

from vantage_cli.printer import Printer, Printable, ContentType
from vantage_cli.commands.util import (
    specific_exception_handler,
    mask_sensitive_string,
    CommandExecutor,
)


# Used to pass API key from configuration.
COMMAND_NAMES = [
    "search-embedding",
    "search-semantic",
    "search-more-like-this",
    "search-more-like-these",
]


def _create_weighted_field_values(
    weighted_field_values: str,
) -> Optional[List[WeightedFieldValueItem]]:
    if weighted_field_values is None:
        return None

    items = []
    try:
        for weight_field in jsonpickle.loads(weighted_field_values):
            items.append(WeightedFieldValueItem.model_validate(weight_field))
    except Exception:
        raise click.BadOptionUsage("Invalid weighted values option.")

    return items


def _create_weight(
    query_key_word_max_overall_weight: Optional[float],
    query_key_word_weighting_mode: Optional[str],
    weighted_field_values_list: Optional[List[WeightedFieldValueItem]],
) -> Optional[FieldValueWeighting]:
    if all(
        value is None
        for value in [
            query_key_word_max_overall_weight,
            query_key_word_weighting_mode,
            weighted_field_values_list,
        ]
    ):
        return None

    FieldValueWeighting(
        query_key_word_max_overall_weight=query_key_word_max_overall_weight,
        query_key_word_weighting_mode=query_key_word_weighting_mode,
        weighted_field_values=weighted_field_values_list,
    )


def _create_pagination(
    page: Optional[int],
    items_per_page: Optional[int],
    pagination_treshold: Optional[int],
) -> Optional[Pagination]:
    if all(
        value is None
        for value in [
            page,
            items_per_page,
            pagination_treshold,
        ]
    ):
        return None

    return Pagination(
        page=page,
        count=items_per_page,
        threshold=pagination_treshold,
    )


def _create_sort(
    sort_field: Optional[str],
    sort_order: Optional[str],
    sort_mode: Optional[str],
) -> Optional[Sort]:
    if all(
        value is None
        for value in [
            sort_field,
            sort_order,
            sort_mode,
        ]
    ):
        return None
    return Sort(
        field=sort_field,
        order=sort_order,
        mode=sort_mode,
    )


def _create_filter(boolean_filter: Optional[str]) -> Optional[Filter]:
    if boolean_filter is None:
        return None

    return Filter(boolean_filter=boolean_filter)


def _create_search_options(
    page: Optional[int],
    items_per_page: Optional[int],
    pagination_treshold: Optional[int],
    sort_field: Optional[str],
    sort_order: Optional[str],
    sort_mode: Optional[str],
    boolean_filter: Optional[str],
    weighted_field_values: str,
    query_key_word_max_overall_weight: Optional[float],
    query_key_word_weighting_mode: Optional[str],
) -> tuple:
    pagination = _create_pagination(
        page=page,
        items_per_page=items_per_page,
        pagination_treshold=pagination_treshold,
    )
    sort = _create_sort(
        field=sort_field,
        order=sort_order,
        mode=sort_mode,
    )
    weighted_field_values_list = _create_weighted_field_values(
        weighted_field_values
    )
    weight = _create_weight(
        query_key_word_max_overall_weight=query_key_word_max_overall_weight,
        query_key_word_weighting_mode=query_key_word_weighting_mode,
        weighted_field_values=weighted_field_values_list,
    )
    boolean_filter = _create_filter(boolean_filter=boolean_filter)

    return [pagination, sort, weight]


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
    default=0.3,
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
@click.option(
    "--sort-field",
    type=click.STRING,
    required=False,
    help="Sorting field.",
)
@click.option(
    "--sort-order",
    type=click.STRING,
    required=False,
    help="Sorting order. Supported values (\"asc\"|\"desc\").",
)
@click.option(
    "--sort-mode",
    type=click.STRING,
    required=False,
    help="Sorting mode. Supported values (\"semantic_threshold\"|\"field_selection\").",
)
@click.option(
    "--pagination-treshold",
    type=click.INT,
    required=False,
    help="Pagination treshold.",
)
@click.option(
    "--query-key-word-max-overall-weight",
    type=click.STRING,
    required=False,
    help="",
)
@click.option(
    "--query-key-word-weighting-mode",
    type=click.STRING,
    required=False,
    help="",
)
@click.option(
    "--weighted-field-values",
    type=click.STRING,
    required=False,
    help="",
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
    sort_field,
    sort_order,
    sort_mode,
    vantage_api_key,
    collection_id,
    pagination_treshold,
    query_key_word_max_overall_weight,
    query_key_word_weighting_mode,
    weighted_field_values,
):
    """Search based on the provided embedding vector."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]
    logger: Logger = ctx["logger"]

    data = {
        "embedding": embedding,
        "accuracy": accuracy,
        "page": page,
        "items_per_page": items_per_page,
        "boolean_filter": boolean_filter,
        "sort_field": sort_field,
        "sort_order": sort_order,
        "sort_mode": sort_mode,
        "vantage_api_key": mask_sensitive_string(vantage_api_key),
        "collection_id": collection_id,
    }
    logger.debug(f"Executing search with data: {data}")

    pagination, sort, weight = _create_search_options(
        page=page,
        items_per_page=items_per_page,
        pagination_treshold=pagination_treshold,
        sort_field=sort_field,
        sort_order=sort_order,
        sort_mode=sort_mode,
        boolean_filter=boolean_filter,
        weighted_field_values=weighted_field_values,
        query_key_word_max_overall_weight=query_key_word_max_overall_weight,
        query_key_word_weighting_mode=query_key_word_weighting_mode,
    )

    executor.execute_and_print_output(
        command=lambda: [
            item.__dict__
            for item in client.embedding_search(
                embedding=jsonpickle.loads(embedding),
                collection_id=collection_id,
                accuracy=accuracy,
                pagination=pagination,
                filter=boolean_filter,
                sort=sort,
                field_value_weighting=weight,
                vantage_api_key=vantage_api_key,
            ).results
        ],
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=NotFoundException,
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
    default=0.3,
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
@click.option(
    "--sort-field",
    type=click.STRING,
    required=False,
    help="Sorting field.",
)
@click.option(
    "--sort-order",
    type=click.STRING,
    required=False,
    help="Sorting order. Supported values (\"asc\"|\"desc\").",
)
@click.option(
    "--sort-mode",
    type=click.STRING,
    required=False,
    help="Sorting mode. Supported values (\"semantic_threshold\"|\"field_selection\").",
)
@click.option(
    "--pagination-treshold",
    type=click.INT,
    required=False,
    help="Pagination treshold.",
)
@click.option(
    "--query-key-word-max-overall-weight",
    type=click.STRING,
    required=False,
    help="",
)
@click.option(
    "--query-key-word-weighting-mode",
    type=click.STRING,
    required=False,
    help="",
)
@click.option(
    "--weighted-field-values",
    type=click.STRING,
    required=False,
    help="",
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
    sort_field,
    sort_order,
    sort_mode,
    vantage_api_key,
    collection_id,
    pagination_treshold,
    query_key_word_max_overall_weight,
    query_key_word_weighting_mode,
    weighted_field_values,
):
    """Search based on the provided text query."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]
    logger: Logger = ctx["logger"]

    data = {
        "text": text,
        "accuracy": accuracy,
        "page": page,
        "items_per_page": items_per_page,
        "boolean_filter": boolean_filter,
        "sort_field": sort_field,
        "sort_order": sort_order,
        "sort_mode": sort_mode,
        "vantage_api_key": mask_sensitive_string(vantage_api_key),
        "collection_id": collection_id,
    }
    logger.debug(f"Executing search with data: {data}")
    pagination, sort, weight = _create_search_options(
        page=page,
        items_per_page=items_per_page,
        pagination_treshold=pagination_treshold,
        sort_field=sort_field,
        sort_order=sort_order,
        sort_mode=sort_mode,
        boolean_filter=boolean_filter,
        weighted_field_values=weighted_field_values,
        query_key_word_max_overall_weight=query_key_word_max_overall_weight,
        query_key_word_weighting_mode=query_key_word_weighting_mode,
    )

    executor.execute_and_print_output(
        command=lambda: [
            item.__dict__
            for item in client.semantic_search(
                text=text,
                collection_id=collection_id,
                accuracy=accuracy,
                pagination=pagination,
                filter=boolean_filter,
                sort=sort,
                field_value_weighting=weight,
                vantage_api_key=vantage_api_key,
            ).results
        ],
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=NotFoundException,
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
    default=0.3,
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
@click.option(
    "--sort-field",
    type=click.STRING,
    required=False,
    help="Sorting field.",
)
@click.option(
    "--sort-order",
    type=click.STRING,
    required=False,
    help="Sorting order. Supported values (\"asc\"|\"desc\").",
)
@click.option(
    "--sort-mode",
    type=click.STRING,
    required=False,
    help="Sorting mode. Supported values (\"semantic_threshold\"|\"field_selection\").",
)
@click.argument(
    "collection_id",
    type=click.STRING,
    required=True,
)
@click.option(
    "--pagination-treshold",
    type=click.INT,
    required=False,
    help="Pagination treshold.",
)
@click.option(
    "--query-key-word-max-overall-weight",
    type=click.STRING,
    required=False,
    help="",
)
@click.option(
    "--query-key-word-weighting-mode",
    type=click.STRING,
    required=False,
    help="",
)
@click.option(
    "--weighted-field-values",
    type=click.STRING,
    required=False,
    help="",
)
@click.pass_obj
def more_like_this_search(
    ctx,
    document_id,
    accuracy,
    page,
    items_per_page,
    boolean_filter,
    sort_field,
    sort_order,
    sort_mode,
    vantage_api_key,
    collection_id,
    pagination_treshold,
    query_key_word_max_overall_weight,
    query_key_word_weighting_mode,
    weighted_field_values,
):
    """Search based on the provided document ID."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]
    logger: Logger = ctx["logger"]

    data = {
        "document_id": document_id,
        "accuracy": accuracy,
        "page": page,
        "items_per_page": items_per_page,
        "boolean_filter": boolean_filter,
        "sort_field": sort_field,
        "sort_order": sort_order,
        "sort_mode": sort_mode,
        "vantage_api_key": mask_sensitive_string(vantage_api_key),
        "collection_id": collection_id,
    }
    logger.debug(f"Executing search with data: {data}")

    pagination, sort, weight = _create_search_options(
        page=page,
        items_per_page=items_per_page,
        pagination_treshold=pagination_treshold,
        sort_field=sort_field,
        sort_order=sort_order,
        sort_mode=sort_mode,
        boolean_filter=boolean_filter,
        weighted_field_values=weighted_field_values,
        query_key_word_max_overall_weight=query_key_word_max_overall_weight,
        query_key_word_weighting_mode=query_key_word_weighting_mode,
    )

    executor.execute_and_print_output(
        command=lambda: [
            item.__dict__
            for item in client.more_like_this_search(
                document_id=document_id,
                collection_id=collection_id,
                accuracy=accuracy,
                pagination=pagination,
                filter=boolean_filter,
                sort=sort,
                field_value_weighting=weight,
                vantage_api_key=vantage_api_key,
            ).results
        ],
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=NotFoundException,
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
    default=0.3,
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
@click.option(
    "--sort-field",
    type=click.STRING,
    required=False,
    help="Sorting field.",
)
@click.option(
    "--sort-order",
    type=click.STRING,
    required=False,
    help="Sorting order. Supported values (\"asc\"|\"desc\").",
)
@click.option(
    "--sort-mode",
    type=click.STRING,
    required=False,
    help="Sorting mode. Supported values (\"semantic_threshold\"|\"field_selection\").",
)
@click.option(
    "--pagination-treshold",
    type=click.INT,
    required=False,
    help="Pagination treshold.",
)
@click.option(
    "--query-key-word-max-overall-weight",
    type=click.STRING,
    required=False,
    help="",
)
@click.option(
    "--query-key-word-weighting-mode",
    type=click.STRING,
    required=False,
    help="",
)
@click.option(
    "--weighted-field-values",
    type=click.STRING,
    required=False,
    help="",
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
    sort_field,
    sort_order,
    sort_mode,
    vantage_api_key,
    collection_id,
    pagination_treshold,
    query_key_word_max_overall_weight,
    query_key_word_weighting_mode,
    weighted_field_values,
):
    """
    Search based on the provided MoreLikeThese items.
    """
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]
    logger: Logger = ctx["logger"]

    try:
        more_like_these = parse_more_like_these(more_like_these_json.read())
    except Exception:
        logger.debug(traceback.format_exc())
        printer.print(
            Printable.stderr(
                content="Invalid JSON input",
                content_type=ContentType.PLAINTEXT,
            )
        )
        return

    data = {
        "more_like_these": more_like_these_json,
        "accuracy": accuracy,
        "page": page,
        "items_per_page": items_per_page,
        "boolean_filter": boolean_filter,
        "sort_field": sort_field,
        "sort_order": sort_order,
        "sort_mode": sort_mode,
        "vantage_api_key": mask_sensitive_string(vantage_api_key),
        "collection_id": collection_id,
    }
    logger.debug(f"Executing search with data: {data}")

    pagination, sort, weight = _create_search_options(
        page=page,
        items_per_page=items_per_page,
        pagination_treshold=pagination_treshold,
        sort_field=sort_field,
        sort_order=sort_order,
        sort_mode=sort_mode,
        boolean_filter=boolean_filter,
        weighted_field_values=weighted_field_values,
        query_key_word_max_overall_weight=query_key_word_max_overall_weight,
        query_key_word_weighting_mode=query_key_word_weighting_mode,
    )

    executor.execute_and_print_output(
        command=lambda: [
            item.__dict__
            for item in client.more_like_these_search(
                more_like_these=more_like_these,
                collection_id=collection_id,
                accuracy=accuracy,
                pagination=pagination,
                filter=boolean_filter,
                sort=sort,
                field_value_weighting=weight,
                vantage_api_key=vantage_api_key,
            ).results
        ],
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=NotFoundException,
            message="Collection not found.",
        ),
    )
