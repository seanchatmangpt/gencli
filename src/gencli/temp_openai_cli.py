import click


@click.group()
def cli():
    pass


@click.command(name="init")
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    type=bool,
    required=False,
    help="Enable verbose output.",
)
@click.argument("session", type=str)
def init(session, **kwargs):
    """Initialize a new chat session."""
    click.echo("Command init executed")


cli.add_command(init)


@click.command(name="send")
@click.option(
    "--timestamp",
    "-t",
    type=bool,
    required=False,
    help="Add a timestamp to the message.",
)
@click.argument("message", type=str)
def send(message):
    """Send a message to the chat."""
    click.echo("Command send executed")


cli.add_command(send)


@click.command(name="history")
@click.option(
    "--limit",
    "-l",
    type=int,
    required=False,
    help="Limit the number of messages to retrieve.",
)
@click.argument("session", type=str)
def history(session):
    """Retrieve the chat history."""
    click.echo("Command history executed")


cli.add_command(history)


@click.command(name="close")
@click.option(
    "--force",
    "-f",
    type=bool,
    required=False,
    help="Forcefully close the session without prompt.",
)
@click.argument("session", type=str)
def close(session):
    """Close the chat session."""
    click.echo("Command close executed")


cli.add_command(close)


@click.command(name="admin")
@click.option("--id", "-i", type=int, required=False, help="ID for admin action.")
@click.argument("action", type=str)
def admin(action):
    """Admin actions."""
    click.echo("Command admin executed")


cli.add_command(admin)


@click.command(name="search")
@click.option(
    "--radius",
    "-r",
    type=float,
    required=False,
    help="Search radius for the vector search.",
)
@click.argument("query", type=str)
def search(query):
    """Perform a vector search."""
    click.echo("Command search executed")


cli.add_command(search)

if __name__ == "__main__":
    cli()
