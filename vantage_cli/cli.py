#!/usr/bin/env python3

"""Console script for vantage_cli."""

import click
from command import CommandParser
from vantage import VantageClient
from printer import Printer, OutputType

DEFAULT_API_HOST = "https://api.dev-a.dev.vantagediscovery.com"
DEFAULT_AUTH_HOST = "https://vantage-dev.us.auth0.com"


@click.command("vantage")
@click.option(
    "-t",
    "--jwt-token",
    envvar="VANTAGE_API_JWT_TOKEN",
    type=click.STRING,
    default=None,
)
@click.option("-a", "--account-id", type=click.STRING, default=None)
@click.option(
    "-c",
    "--command",
    type=click.Choice(
        [
            "get-account",
            "update-account",
            "get-vantage-api-key",
            "get-vantage-api-keys",
            "create-external-api-key",
            "get-external-api-key",
            "get-external-api-keys",
            "update-external-api-key",
            "delete-external-api-key",
            "list-collections",
            "create-collection",
            "get-collection",
            "update-collection",
            "delete-collection",
            "upload-embedding",  # This is most likely impractical for CLI
            "upload-embedding-by-path",
            "embedding-search",
            "semantic-search",
            "more-like-this-search",
            "more-like-these-search",
            "upload-documents-from-jsonl",  # This is most likely impractical for CLI
            "upload-documents-from-path",
        ]
    ),
)
@click.option(
    "-o", "--output-type", type=click.Choice(["json", "csv"]), default="json"
)
@click.argument("command_arguments", nargs=-1)
def main(jwt_token, account_id, command, command_arguments, output_type):
    client = VantageClient.using_jwt_token(
        vantage_api_jwt_token=jwt_token,
        api_host=DEFAULT_API_HOST,
        account_id=account_id,
    )

    parser = CommandParser(client=client)
    printer = Printer(output_type=OutputType[output_type.upper()])
    command = parser.parse(
        command=command,
        account_id=account_id,
        command_arguments=command_arguments,
    )
    click.echo(printer.parse(command.execute()))


if __name__ == "__main__":
    main()  # pragma: no cover
