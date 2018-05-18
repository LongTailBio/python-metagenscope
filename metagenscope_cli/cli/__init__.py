"""MetaGenScope CLI."""

import click

from .add_cli import create, add
from .auth_cli import register, login, status
from .get_cli import get
from .run_cli import run
from .upload_cli import upload


@click.group()
def main():
    """Use to interact with the MetaGenScope web platform."""
    pass


main.add_command(register)
main.add_command(login)
main.add_command(status)
main.add_command(get)
main.add_command(run)
main.add_command(upload)
main.add_command(create)
main.add_command(add)
