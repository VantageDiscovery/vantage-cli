#!/usr/bin/env python3

"""Console script for vantage_cli."""

import click
from commands.account import get_account, update_account
from commands.api_keys import (
    get_vantage_api_key,
    get_vantage_api_keys,
    create_external_api_key,
    get_external_api_keys,
    get_external_api_key,
)
from vantage_cli.util import create_client, create_printer


@click.group()
@click.option(
    "-a",
    "--account-id",
    envvar="VANTAGE_ACCOUNT_ID",
    type=click.STRING,
    default=None,
)
@click.option(
    "-t",
    "--jwt-token",
    envvar="VANTAGE_API_JWT_TOKEN",
    type=click.STRING,
    default=None,
)
@click.option(
    "-o", "--output-type", type=click.Choice(["json", "csv"]), default="json"
)
@click.pass_context
def cli(ctx, account_id, jwt_token, output_type):
    ctx.ensure_object(dict)
    ctx.obj["client"] = create_client(
        jwt_token=jwt_token, account_id=account_id
    )
    ctx.obj["printer"] = create_printer(output_type=output_type)


cli.add_command(get_account)
cli.add_command(update_account)
cli.add_command(get_vantage_api_key)
cli.add_command(get_vantage_api_keys)
cli.add_command(create_external_api_key)
cli.add_command(get_external_api_keys)
cli.add_command(get_external_api_key)

if __name__ == "__main__":
    cli()  # pragma: no cover
