import click
from printer import Printable, ContentType


@click.command("get-vantage-api-keys")
@click.pass_obj
def get_vantage_api_keys(ctx):
    """Fetches Vantage API keys from an account."""
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
    Fetches a specific Vantage API key from an account.

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
    Fetches a specific Vantage API key from an account.

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
    """Fetches external API keys from an account."""
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
    Fetches a specific external API key from an account.

    id: External API key ID.
    """
    client = ctx["client"]
    printer = ctx["printer"]

    response = Printable(
        content=client.get_external_api_key(external_key_id=key_id).__dict__,
        content_type=ContentType.OBJECT,
    )
    printer.print(response)
