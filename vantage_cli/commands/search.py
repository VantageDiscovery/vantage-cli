import click


@click.command("embedding-search", help="Not Implemented.")
@click.pass_obj
def embedding_search(ctx):
    """Search using provided embeddings."""
    click.echo("Not implemented.")


@click.command("semantic-search", help="Not Implemented.")
@click.pass_obj
def semantic_search(ctx):
    """Seartch using text."""
    click.echo("Not implemented.")


@click.command("more-like-this-search", help="Not Implemented.")
@click.pass_obj
def more_like_this_search(ctx):
    """Finds more like this."""
    click.echo("Not implemented.")


@click.command("more-like-these-search", help="Not Implemented.")
@click.pass_obj
def more_like_these_search(ctx):
    """Finds more like these."""
    click.echo("Not implemented.")
