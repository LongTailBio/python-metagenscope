"""MetaGenScope CLI."""

import click
import click_log

from metagenscope_cli.extensions import logger

from .auth_cli import register, login, status
from .get_cli import get
from .run_cli import run
from .upload_cli import upload


click_log.basic_config(logger)


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
