#!/usr/bin/env python3

"""Console script for vantage_cli."""

import sys
import click
from vantage_cli.commands.account import get_account, update_account
from vantage_cli.commands.api_keys import (
    get_vantage_api_key,
    get_vantage_api_keys,
    create_external_api_key,
    get_external_api_keys,
    get_external_api_key,
    update_external_api_key,
    delete_external_api_key,
)
from vantage_cli.commands.collections import (
    create_collection_upe,
    create_collection_openai,
    create_collection_hf,
    delete_collection,
    get_collection,
    list_collections,
    update_collection,
)
from vantage_cli.commands.documents import (
    upsert_documents_from_parquet,
    upsert_documents_from_jsonl,
    delete_documents,
)
from vantage_cli.commands.search import (
    embedding_search,
    more_like_these_search,
    more_like_this_search,
    semantic_search,
)
from vantage_cli.printer import create_printer
from vantage_sdk.client import VantageClient
from vantage_cli.commands.util import CommandExecutor, mask_sensitive_string
from vantage_cli.config import (
    default_config_file,
    configuration_callback,
)
import logging

_LOGGER_FORMAT = "[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s:%(lineno)d] %(message)s"
_LOGGER_DATE_FORMAT = "%d/%b/%Y %H:%M:%S"

DEFAULT_API_HOST = "https://api.vanta.ge"
DEFAULT_AUTH_HOST = "https://auth.vanta.ge"


def create_client_from_vantage_api_key(
    vantage_api_key: str, account_id: str, api_host: str
):
    return VantageClient.using_vantage_api_key(
        vantage_api_key=vantage_api_key,
        api_host=api_host,
        account_id=account_id,
    )


def create_client_from_jwt(jwt_token: str, account_id: str, api_host: str):
    return VantageClient.using_jwt_token(
        vantage_api_jwt_token=jwt_token,
        api_host=api_host,
        account_id=account_id,
    )


def create_client_from_credentials(
    account_id: str,
    client_id: str,
    client_secret: str,
    api_host: str,
    auth_host: str,
):
    return VantageClient.using_client_credentials(
        vantage_client_id=client_id,
        vantage_client_secret=client_secret,
        api_host=api_host,
        auth_host=auth_host,
        account_id=account_id,
    )


def create_executor(debug: bool, logger: logging.Logger):
    return CommandExecutor(debug=debug, logger=logger)


def configure_debug_logger(debug: bool) -> logging.Logger:
    if debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format=_LOGGER_FORMAT,
        datefmt=_LOGGER_DATE_FORMAT,
        stream=sys.stderr,
    )
    return logging.getLogger("vantage")


@click.group(invoke_without_command=True)
@click.option(
    "-c",
    "--config-file",
    type=click.Path(),
    default=default_config_file(),
    required=False,
    callback=configuration_callback,
    is_eager=True,
    help="Path to config file.",
)
@click.option(
    "-a",
    "--account-id",
    envvar="VANTAGE_ACCOUNT_ID",
    type=click.STRING,
    default=None,
    help="Vantage account ID",
)
@click.option(
    "-d",
    "--debug",
    type=click.BOOL,
    default=False,
    is_flag=True,
    help="Print execution debug info.",
)
@click.option(
    "-k",
    "--vantage-api-key",
    envvar="VANTAGE_API_KEY",
    type=click.STRING,
    default=None,
    required=False,
    help="Vantage API key for accessing API.",
)
@click.option(
    "-t",
    "--jwt-token",
    envvar="VANTAGE_API_JWT_TOKEN",
    type=click.STRING,
    default=None,
    required=False,
    help="JWT token for accessing API.",
)
@click.option(
    "-i",
    "--client-id",
    envvar="VANTAGE_API_CLIENT_ID",
    type=click.STRING,
    default=None,
    required=False,
    help="Client API ID.",
)
@click.option(
    "-s",
    "--client-secret",
    envvar="VANTAGE_API_CLIENT_SECRET",
    type=click.STRING,
    default=None,
    required=False,
    help="Client API secret.",
)
@click.option(
    "-o",
    "--output-type",
    type=click.Choice(["json", "csv"]),
    default="json",
    help="Command execution result print format.",
)
@click.option(
    "--api-host",
    type=click.STRING,
    default=DEFAULT_API_HOST,
    envvar="VANTAGE_API_HOST",
    help="Specify non-default API host (used for development).",
)
@click.option(
    "--auth-host",
    type=click.STRING,
    default=DEFAULT_AUTH_HOST,
    envvar="VANTAGE_AUTH_HOST",
    help="Specify non-default auth host (used for development).",
)
@click.option(
    "-v",
    "--version",
    type=click.BOOL,
    default=False,
    is_flag=True,
    help="Print application version.",
)
@click.pass_context
def cli(
    ctx,
    account_id,
    vantage_api_key,
    jwt_token,
    output_type,
    debug,
    api_host,
    auth_host,
    client_id,
    client_secret,
    config_file,
    version,
):
    ctx.ensure_object(dict)
    logger = configure_debug_logger(debug)

    if version:
        import vantage_cli

        click.echo(vantage_cli.__version__)
        sys.exit(0)

    if ctx.invoked_subcommand is None:
        click.echo(
            f"No command specified. Run {ctx.info_name} --help for help."
        )
        sys.exit(1)

    logger.debug(f"Invoked command {ctx.invoked_subcommand}")
    logger.debug(f"Using API host: {api_host}")
    logger.debug(f"Using account ID: {account_id}")

    client = None

    if vantage_api_key:
        logger.debug(
            f"Creating client using API key: {mask_sensitive_string(vantage_api_key)}"
        )
        client = create_client_from_vantage_api_key(
            vantage_api_key=vantage_api_key,
            account_id=account_id,
            api_host=api_host,
        )
    elif jwt_token:
        logger.debug("Creating client using JWT Token.")
        client = create_client_from_jwt(
            jwt_token=jwt_token,
            account_id=account_id,
            api_host=api_host,
        )
    elif client_id and client_secret:
        logger.debug("Creating client using Client ID/secret pair.")
        logger.debug(f"Using auth host: {auth_host}")
        client = create_client_from_credentials(
            account_id=account_id,
            client_id=client_id,
            client_secret=client_secret,
            api_host=api_host,
            auth_host=auth_host,
        )

    if client is None:
        click.echo(
            "Either Vantage API ket, JWT token or client ID and secret need to be specified."
        )
        exit(127)

    ctx.obj["client"] = client
    ctx.obj["printer"] = create_printer(output_type=output_type)
    ctx.obj["executor"] = create_executor(debug=debug, logger=logger)
    ctx.obj["logger"] = logger


cli.add_command(get_account)
cli.add_command(update_account)
cli.add_command(get_vantage_api_key)
cli.add_command(get_vantage_api_keys)
cli.add_command(create_external_api_key)
cli.add_command(get_external_api_keys)
cli.add_command(get_external_api_key)
cli.add_command(update_external_api_key)
cli.add_command(delete_external_api_key)
cli.add_command(create_collection_upe)
cli.add_command(create_collection_openai)
cli.add_command(create_collection_hf)
cli.add_command(delete_collection)
cli.add_command(get_collection)
cli.add_command(list_collections)
cli.add_command(update_collection)
cli.add_command(upsert_documents_from_parquet)
cli.add_command(upsert_documents_from_jsonl)
cli.add_command(delete_documents)
cli.add_command(embedding_search)
cli.add_command(more_like_these_search)
cli.add_command(more_like_this_search)
cli.add_command(semantic_search)

if __name__ == "__main__":
    cli()  # pragma: no cover
