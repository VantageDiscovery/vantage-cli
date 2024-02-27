import click


@click.command("list-collections")
@click.pass_obj
def list_collections(ctx):
    """Lists existing colections."""
    click.echo("Not implemented.")


@click.command("create-collection")
@click.pass_obj
def create_collection(ctx):
    """Creates a new collection."""
    click.echo("Not implemented.")


@click.command("get-collection")
@click.pass_obj
def get_collection(ctx):
    """Fetches collection details."""
    click.echo("Not implemented.")


@click.command("update-collection")
@click.pass_obj
def update_collection(ctx):
    """Updates a collection."""
    click.echo("Not implemented.")


@click.command("delete-collection")
@click.pass_obj
def delete_collection(ctx):
    """Deletes a collection."""
    click.echo("Not implemented.")
