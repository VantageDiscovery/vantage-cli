#!/usr/bin/env python3

"""Console script for vantage_cli."""

import click
import click_config_file
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
from commands.collections import (
    create_collection,
    delete_collection,
    get_collection,
    list_collections,
    update_collection,
)
from commands.upload import upload_parquet, upload_documents
from commands.search import (
    embedding_search,
    more_like_these_search,
    more_like_this_search,
    semantic_search,
)
from vantage_cli.printer import create_printer
from vantage import VantageClient
from vantage_cli.commands.util import CommandExecutor

DEFAULT_API_HOST = "https://api.stage-a.dev.vantagediscovery.com"
DEFAULT_AUTH_HOST = "https://vantage-dev.us.auth0.com"


def create_client_from_jwt(jwt_token: str, account_id: str):
    return VantageClient.using_jwt_token(
        vantage_api_jwt_token=jwt_token,
        api_host=DEFAULT_API_HOST,
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


def create_executor(debug: bool):
    return CommandExecutor(debug_exceptions=debug)


@click.group()
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
    "--debug-errors",
    type=click.BOOL,
    default=False,
    is_flag=True,
    help="Print debug info for errors returned by API.",
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
    help="Specify non-default API host (used for development).",
)
@click.option(
    "--auth-host",
    type=click.STRING,
    default=DEFAULT_AUTH_HOST,
    help="Specify non-default auth host (used for development).",
)
@click.pass_context
def cli(
    ctx,
    account_id,
    jwt_token,
    output_type,
    debug_errors,
    api_host,
    auth_host,
    client_id,
    client_secret,
):
    ctx.ensure_object(dict)

    client = None

    if jwt_token is not None:
        client = create_client_from_jwt(
            jwt_token=jwt_token, account_id=account_id
        )
    elif client_id is not None and client_secret is not None:
        client = create_client_from_credentials(
            account_id=account_id,
            client_id=client_id,
            client_secret=client_secret,
            api_host=api_host,
            auth_host=auth_host,
        )

    if client is None:
        click.echo(
            "Either JWT token or client ID and secret need to be specified."
        )
        exit(127)

    ctx.obj["client"] = client
    ctx.obj["printer"] = create_printer(output_type=output_type)
    ctx.obj["executor"] = create_executor(debug=debug_errors)


cli.add_command(get_account)
cli.add_command(update_account)
cli.add_command(get_vantage_api_key)
cli.add_command(get_vantage_api_keys)
cli.add_command(create_external_api_key)
cli.add_command(get_external_api_keys)
cli.add_command(get_external_api_key)
cli.add_command(update_external_api_key)
cli.add_command(delete_external_api_key)
cli.add_command(create_collection)
cli.add_command(delete_collection)
cli.add_command(get_collection)
cli.add_command(list_collections)
cli.add_command(update_collection)
cli.add_command(upload_parquet)
cli.add_command(upload_documents)
cli.add_command(embedding_search)
cli.add_command(more_like_these_search)
cli.add_command(more_like_this_search)
cli.add_command(semantic_search)

if __name__ == "__main__":
    cli()  # pragma: no cover
