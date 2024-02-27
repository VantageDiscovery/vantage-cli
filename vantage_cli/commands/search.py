import click


@click.command("embedding-search")
@click.pass_obj
def embedding_search(ctx):
    click.echo("Not implemented.")


@click.command("semantic-search")
@click.pass_obj
def semantic_search(ctx):
    click.echo("Not implemented.")


@click.command("more-like-this-search")
@click.pass_obj
def more_like_this_search(ctx):
    click.echo("Not implemented.")


@click.command("more-like-these-search")
@click.pass_obj
def more_like_these_search(ctx):
    click.echo("Not implemented.")
