from logging import Logger
import click
from vantage_cli.printer import ContentType, Printer
from vantage_sdk.client import VantageClient
from vantage_sdk.core.http.exceptions import NotFoundException
from vantage_cli.commands.util import (
    specific_exception_handler,
    mask_sensitive_string,
    CommandExecutor,
)


@click.command("get-vantage-api-keys")
@click.pass_obj
def get_vantage_api_keys(ctx):
    """Lists existing Vantage API keys."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]
    logger: Logger = ctx["logger"]

    logger.debug("Fetching API keys data...")
    executor.execute_and_print_output(
        command=lambda: [
            item.__dict__ for item in client.get_vantage_api_keys()
        ],
        output_type=ContentType.OBJECT,
        printer=printer,
    )


@click.command("get-vantage-api-key")
@click.argument(
    "vantage_api_key_id",
    type=click.STRING,
    required=True,
)
@click.pass_obj
def get_vantage_api_key(ctx, vantage_api_key_id):
    """Shows a specific Vantage API key details."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]
    logger: Logger = ctx["logger"]

    logger.debug(
        f"Fetching details for API key ID: {mask_sensitive_string(vantage_api_key_id)}"
    )
    executor.execute_and_print_output(
        command=lambda: client.get_vantage_api_key(
            vantage_api_key_id=vantage_api_key_id
        ).__dict__,
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=NotFoundException,
            message="Vantage API key not found.",
        ),
    )


@click.command("create-external-api-key")
@click.option(
    "--llm-provider",
    type=click.STRING,
    required=True,
    help="LLM provider ID supported by Vantage (\"OpenAPI\"|\"Hugging\").",
)
@click.option(
    "--llm-secret",
    type=click.STRING,
    required=True,
    help="Secret key used to access LLM provider's API.",
)
@click.option(
    "--url",
    type=click.STRING,
    required=False,
    help="Currently not used.",
)
@click.pass_obj
def create_external_api_key(ctx, llm_provider, llm_secret, url):
    """Creates a new external API key."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]
    logger: Logger = ctx["logger"]

    data = {
        "llm_provider": llm_provider,
        "llm_secret": mask_sensitive_string(llm_secret),
        "url": url,
    }
    logger.debug(f"Creating external key with data {data}")
    executor.execute_and_print_output(
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
    executor: CommandExecutor = ctx["executor"]
    logger: Logger = ctx["logger"]

    logger.debug("Fetching external API keys...")
    executor.execute_and_print_output(
        command=lambda: [
            item.__dict__ for item in client.get_external_api_keys()
        ],
        output_type=ContentType.OBJECT,
        printer=printer,
    )


@click.command("get-external-api-key")
@click.argument(
    "external_key_id",
    type=click.STRING,
    required=True,
)
@click.pass_obj
def get_external_api_key(ctx, external_key_id):
    """Shows a specific external API key details."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]
    logger: Logger = ctx["logger"]

    logger.debug(f"Fetching details for key with ID: {external_key_id}")
    executor.execute_and_print_output(
        command=lambda: client.get_external_api_key(
            external_key_id=external_key_id
        ).__dict__,
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=NotFoundException,
            message="External API key not found.",
        ),
    )


@click.command("update-external-api-key")
@click.option(
    "--llm-provider",
    type=click.STRING,
    required=False,
    help="LLM provider ID supported by Vantage (\"OpenAPI\"|\"Hugging\").",
)
@click.option(
    "--llm-secret",
    type=click.STRING,
    required=False,
    help="Secret key used to access LLM provider's API.",
)
@click.option(
    "--url",
    type=click.STRING,
    required=False,
    help="Currently not used.",
)
@click.argument(
    "external_key_id",
    type=click.STRING,
    required=True,
)
@click.pass_obj
def update_external_api_key(
    ctx, llm_provider, llm_secret, url, external_key_id
):
    """Updates external API key data."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]
    logger: Logger = ctx["logger"]

    data = {
        "llm_provider": llm_provider,
        "llm_secret": mask_sensitive_string(llm_secret),
        "url": url,
    }
    logger.debug(f"Updating external key {external_key_id} with data: {data}")
    executor.execute_and_print_output(
        command=lambda: client.update_external_api_key(
            external_key_id=external_key_id,
            url=url,
            llm_provider=llm_provider,
            llm_secret=llm_secret,
        ).__dict__,
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=NotFoundException,
            message="External API key not found.",
        ),
    )


@click.command("delete-external-api-key")
@click.argument(
    "external_key_id",
    type=click.STRING,
    required=True,
)
@click.pass_obj
def delete_external_api_key(ctx, external_key_id):
    """Deletes an external API key."""
    client: VantageClient = ctx["client"]
    printer: Printer = ctx["printer"]
    executor: CommandExecutor = ctx["executor"]
    logger: Logger = ctx["logger"]

    logger.debug(f"Deleting external key {external_key_id}.")
    executor.execute_and_print_output(
        command=lambda: client.delete_external_api_key(
            external_key_id=external_key_id
        ).__dict__,
        output_type=ContentType.OBJECT,
        printer=printer,
        exception_handler=lambda exception: specific_exception_handler(
            exception=exception,
            class_type=NotFoundException,
            message="External API key not found.",
        ),
    )
