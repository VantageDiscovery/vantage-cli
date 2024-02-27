import click
from printer import Printable, ContentType


@click.command("get-vantage-api-keys")
@click.pass_obj
def get_vantage_api_keys(ctx):
    """Lists existing Vantage API keys."""
    client = ctx["client"]
    printer = ctx["printer"]

    response = Printable(
        content=[item.__dict__ for item in client.get_vantage_api_keys()],
        content_type=ContentType.OBJECT,
    )
    printer.print(response)


@click.command("get-vantage-api-key")
@click.argument("key_id", type=click.STRING)
@click.pass_obj
def get_vantage_api_key(ctx, key_id):
    """
    Shows a specific Vantage API key details.

    id: Vantage API key ID.
    """
    client = ctx["client"]
    printer = ctx["printer"]

    response = Printable(
        content=client.get_vantage_api_key(vantage_api_key_id=key_id).__dict__,
        content_type=ContentType.OBJECT,
    )
    printer.print(response)


@click.command("create-external-api-key")
@click.option("--llm-provider", type=click.STRING)
@click.option("--llm-secret", type=click.STRING)
@click.option("--url", type=click.STRING, required=False)
@click.pass_obj
def create_external_api_key(ctx, llm_provider, llm_secret, url):
    """
    Creates new external API key.

    id: Vantage API key ID.
    """
    client = ctx["client"]
    printer = ctx["printer"]

    response = Printable(
        content=client.create_external_api_key(
            llm_provider=llm_provider,
            llm_secret=llm_secret,
            url=url,
        ).__dict__,
        content_type=ContentType.OBJECT,
    )
    printer.print(response)


@click.command("get-external-api-keys")
@click.pass_obj
def get_external_api_keys(ctx):
    """Lists existing external API keys."""
    client = ctx["client"]
    printer = ctx["printer"]

    response = Printable(
        content=[item.__dict__ for item in client.get_external_api_keys()],
        content_type=ContentType.OBJECT,
    )
    printer.print(response)


@click.command("get-external-api-key")
@click.argument("key_id", type=click.STRING)
@click.pass_obj
def get_external_api_key(ctx, key_id):
    """
    Shows a specific external API key details.

    id: External API key ID.
    """
    client = ctx["client"]
    printer = ctx["printer"]

    response = Printable(
        content=client.get_external_api_key(external_key_id=key_id).__dict__,
        content_type=ContentType.OBJECT,
    )
    printer.print(response)


@click.command("update-external-api-key")
@click.pass_obj
def update_external_api_key(ctx):
    """Updates external API key data."""
    click.echo("Not implemented.")


@click.command("delete-external-api-key")
@click.pass_obj
def delete_external_api_key(ctx):
    """Deletes external API key."""
    click.echo("Not implemented.")
