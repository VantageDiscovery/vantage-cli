import click
from printer import Printer, Printable, ContentType
from vantage import VantageClient
from vantage_cli.util import get_generic_message_for_exception
from vantage.exceptions import VantageNotFoundError


@click.command("get-vantage-api-keys")
@click.pass_obj
def get_vantage_api_keys(ctx):
    """Lists existing Vantage API keys."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]

    content_type = ContentType.OBJECT
    try:
        content = [item.__dict__ for item in client.get_vantage_api_keys()]
    except Exception as exception:
        content = get_generic_message_for_exception(exception)
        content_type = ContentType.PLAINTEXT

    printer.print(
        Printable(
            content=content,
            content_type=content_type,
        )
    )


@click.command("get-vantage-api-key")
@click.argument("key_id", type=click.STRING)
@click.pass_obj
def get_vantage_api_key(ctx, key_id):
    """Shows a specific Vantage API key details."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]

    content_type = ContentType.OBJECT
    try:
        content = client.get_vantage_api_key(
            vantage_api_key_id=key_id
        ).__dict__
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


@click.command("create-external-api-key")
@click.option(
    "--llm-provider",
    type=click.STRING,
    help="LLM provider ID supported by Vantage. Currently either \"OpenAPI\" or \"Hugging\".",
)
@click.option(
    "--llm-secret",
    type=click.STRING,
    help="Secret key used to access LLM provider's API",
)
@click.option(
    "--url", type=click.STRING, required=False, help="Currently not used"
)
@click.pass_obj
def create_external_api_key(ctx, llm_provider, llm_secret, url):
    """Creates new external API key."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]

    content_type = ContentType.OBJECT
    try:
        content = client.create_external_api_key(
            llm_provider=llm_provider,
            llm_secret=llm_secret,
            url=url,
        ).__dict__
    except Exception as exception:
        content = get_generic_message_for_exception(exception)
        content_type = ContentType.PLAINTEXT

    printer.print(
        Printable(
            content=content,
            content_type=content_type,
        )
    )


@click.command("get-external-api-keys")
@click.pass_obj
def get_external_api_keys(ctx):
    """Lists existing external API keys."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]

    content_type = ContentType.OBJECT
    try:
        content = [item.__dict__ for item in client.get_external_api_keys()]
    except Exception as exception:
        content = get_generic_message_for_exception(exception)
        content_type = ContentType.PLAINTEXT

    printer.print(
        Printable(
            content=content,
            content_type=content_type,
        )
    )


@click.command("get-external-api-key")
@click.argument("key_id", type=click.STRING)
@click.pass_obj
def get_external_api_key(ctx, key_id):
    """Shows a specific external API key details."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]

    content_type = ContentType.OBJECT
    try:
        content = client.get_external_api_key(external_key_id=key_id).__dict__
    except Exception as exception:
        if isinstance(exception, VantageNotFoundError):
            content = "External API key not found."
        else:
            content = get_generic_message_for_exception(exception)
        content_type = ContentType.PLAINTEXT

    printer.print(
        Printable(
            content=content,
            content_type=content_type,
        )
    )


@click.command("update-external-api-key")
@click.option(
    "--llm-provider",
    type=click.STRING,
    help="LLM provider ID supported by Vantage. Currently either \"OpenAPI\" or \"Hugging\".",
)
@click.option(
    "--llm-secret",
    type=click.STRING,
    help="Secret key used to access LLM provider's API",
)
@click.option(
    "--url", type=click.STRING, required=False, help="Currently not used"
)
@click.argument("key_id", type=click.STRING)
@click.pass_obj
def update_external_api_key(ctx, llm_provider, llm_secret, url, key_id):
    """Updates external API key data."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]

    content_type = ContentType.OBJECT
    try:
        content = client.update_external_api_key(
            external_key_id=key_id,
            url=url,
            llm_provider=llm_provider,
            llm_secret=llm_secret,
        ).__dict__
    except Exception as exception:
        if isinstance(exception, VantageNotFoundError):
            content = "External API key not found."
        else:
            content = get_generic_message_for_exception(exception)
        content_type = ContentType.PLAINTEXT

    printer.print(
        Printable(
            content=content,
            content_type=content_type,
        )
    )


@click.command("delete-external-api-key")
@click.argument("key_id", type=click.STRING)
@click.pass_obj
def delete_external_api_key(ctx, key_id):
    """Deletes external API key."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]

    content_type = ContentType.OBJECT
    try:
        content = client.delete_external_api_key(
            external_key_id=key_id
        ).__dict__
    except Exception as exception:
        if isinstance(exception, VantageNotFoundError):
            content = "External API key not found."
        else:
            content = get_generic_message_for_exception(exception)
        content_type = ContentType.PLAINTEXT

    printer.print(
        Printable(
            content=content,
            content_type=content_type,
        )
    )
