
import click

@click.group()
def cli():
    pass


@click.command(name='create')

@click.option('--item', type=str,
required=True,
help='Name of the item')

@click.option('--value', type=str,
required=True,
help='Value of the item')

def create(item, value):
    """Create a new item."""
    click.echo('Command create executed.')

cli.add_command(create)

@click.command(name='read')

@click.option('--item', type=str,
required=True,
help='Name of the item')

def read(item):
    """Read an item."""
    click.echo('Command read executed.')

cli.add_command(read)

@click.command(name='update')

@click.option('--item', type=str,
required=True,
help='Name of the item')

@click.option('--new_value', type=str,
required=True,
help='New value of the item')

def update(item, new_value):
    """Update an item."""
    click.echo('Command update executed.')

cli.add_command(update)

@click.command(name='delete')

@click.option('--item', type=str,
required=True,
help='Name of the item')

def delete(item):
    """Delete an item."""
    click.echo('Command delete executed.')

cli.add_command(delete)


if __name__ == '__main__':
    cli()