import click


@click.command("upload-parquet")
@click.pass_obj
def upload_embedding(ctx):
    # TODO: implement uploading both from file and stdin
    click.echo("Not implemented.")


@click.command("upload-documents")
@click.pass_obj
def upload_documents(ctx):
    # TODO: implement uploading both from file and stdin
    click.echo("Not implemented.")
