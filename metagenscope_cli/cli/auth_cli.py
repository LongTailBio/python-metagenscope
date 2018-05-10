"""CLI to login, register and authenticate."""

import click
from requests.exceptions import HTTPError

from metagenscope_cli.network.authenticator import Authenticator
from metagenscope_cli.config import config

from .cli import main


@main.command()
@click.option('-h', '--host', default=None)
@click.argument('username')
@click.argument('user_email')
@click.argument('password')
def register(host, username, user_email, password):
    """Register as a new MetaGenScope user."""
    authenticator = Authenticator(host=host)
    try:
        jwt_token = authenticator.register(username, user_email, password)
        click.echo(f'JWT Token: {jwt_token}')
    except HTTPError as http_error:
        click.echo(f'There was an error with registration: {http_error}', err=True)

    # TODO: ask to persist JWT here


@main.command()
@click.option('-h', '--host', default=None)
@click.argument('user_email')
@click.argument('password')
def login(host, user_email, password):
    """Authenticate as an existing MetaGenScope user."""
    authenticator = Authenticator(host=host)
    try:
        jwt_token = authenticator.login(user_email, password)
        click.echo(f'JWT Token: {jwt_token}')

        if click.confirm('Store token for future use (overwrites existing)?'):
            config.set_token(jwt_token)
    except HTTPError as http_error:
        click.echo(f'There was an error logging in: {http_error}', err=True)

    # TODO: ask to persist JWT here


@main.command()
@add_authorization()
def status(uploader):
    """Get user status."""
    response = uploader.knex.get('/api/v1/auth/status')
    click.echo(response)
