import click
from printer import ContentType, Printer
from vantage import VantageClient
from vantage.exceptions import VantageNotFoundError
from vantage_cli.commands.util import specific_exception_handler


@click.command("get-vantage-api-keys")
@click.pass_obj
def get_vantage_api_keys(ctx):
    """Lists existing Vantage API keys."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor = ctx["executor"]

    executor.execute_and_print_output(
        command=lambda: [
            item.__dict__ for item in client.get_vantage_api_keys()
        ],
        output_type=ContentType.OBJECT,
        printer=printer,
    )


@click.command("get-vantage-api-key")
@click.argument(
    "key_id",
    type=click.STRING,
    required=True,
)
@click.pass_obj
def get_vantage_api_key(ctx, key_id):
    """Shows a specific Vantage API key details."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor = ctx["executor"]

    executor.execute_and_print_output(
        command=lambda: client.get_vantage_api_key(
            vantage_api_key_id=key_id
        ).__dict__,
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=VantageNotFoundError,
            message="Vantage API key not found.",
        ),
    )


@click.command("create-external-api-key")
@click.option(
    "--llm-provider",
    type=click.STRING,
    required=True,
    help="LLM provider ID supported by Vantage. Currently either \"OpenAPI\" or \"Hugging\".",
)
@click.option(
    "--llm-secret",
    type=click.STRING,
    required=True,
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

    execute_and_print_output(
        command=lambda: client.create_external_api_key(
            llm_provider=llm_provider,
            llm_secret=llm_secret,
            url=url,
        ).__dict__,
        output_type=ContentType.OBJECT,
        printer=printer,
    )


@click.command("get-external-api-keys")
@click.pass_obj
def get_external_api_keys(ctx):
    """Lists existing external API keys."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]

    execute_and_print_output(
        command=lambda: [
            item.__dict__ for item in client.get_external_api_keys()
        ],
        output_type=ContentType.OBJECT,
        printer=printer,
    )


@click.command("get-external-api-key")
@click.argument(
    "key_id",
    type=click.STRING,
    required=True,
)
@click.pass_obj
def get_external_api_key(ctx, key_id):
    """Shows a specific external API key details."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]

    execute_and_print_output(
        command=lambda: client.get_external_api_key(
            external_key_id=key_id
        ).__dict__,
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=VantageNotFoundError,
            message="External API key not found.",
        ),
    )


@click.command("update-external-api-key")
@click.option(
    "--llm-provider",
    type=click.STRING,
    required=True,
    help="LLM provider ID supported by Vantage. Currently either \"OpenAPI\" or \"Hugging\".",
)
@click.option(
    "--llm-secret",
    type=click.STRING,
    required=True,
    help="Secret key used to access LLM provider's API",
)
@click.option(
    "--url", type=click.STRING, required=False, help="Currently not used"
)
@click.argument("key_id", type=click.STRING, required=True)
@click.pass_obj
def update_external_api_key(ctx, llm_provider, llm_secret, url, key_id):
    """Updates external API key data."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]

    execute_and_print_output(
        command=lambda: client.update_external_api_key(
            external_key_id=key_id,
            url=url,
            llm_provider=llm_provider,
            llm_secret=llm_secret,
        ).__dict__,
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=VantageNotFoundError,
            message="External API key not found.",
        ),
    )


@click.command("delete-external-api-key")
@click.argument(
    "key_id",
    type=click.STRING,
    required=True,
)
@click.pass_obj
def delete_external_api_key(ctx, key_id):
    """Deletes external API key."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]

    execute_and_print_output(
        command=lambda: client.delete_external_api_key(
            external_key_id=key_id
        ).__dict__,
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=VantageNotFoundError,
            message="External API key not found.",
        ),
    )
