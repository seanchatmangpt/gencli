from pathlib import Path

import click


@click.group()
def cli():
    pass


@click.command()
def init():
    pyproject_path = Path("pyproject.toml")

    if pyproject_path.exists():
        raise click.ClickException(
            "A pyproject.toml file already exists in the current directory."
        )

    with pyproject_path.open("w") as f:
        f.write("[build-system]\n")
        f.write('requires = ["setuptools", "wheel"]\n')
        f.write('build-backend = "setuptools.build_meta"\n')

    click.echo(f"Initialized project: {pyproject_path.absolute()}")


@click.command()
def build():
    click.echo("Build project.")


@click.command()
def validate():
    click.echo("Validate project.")


@click.command()
def test():
    click.echo("Test project.")


@click.command()
def deploy():
    click.echo("Deploy project.")


cli.add_command(init)
cli.add_command(build)
cli.add_command(validate)
cli.add_command(test)
cli.add_command(deploy)

if __name__ == "__main__":
    cli()
