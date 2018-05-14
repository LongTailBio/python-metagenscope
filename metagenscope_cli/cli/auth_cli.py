"""CLI to login, register and authenticate."""

import os
import click
import click_log
from requests.exceptions import HTTPError

from metagenscope_cli.extensions import logger
from metagenscope_cli.network.authenticator import Authenticator
from metagenscope_cli.config import config

from .utils import add_authorization


def handle_auth_request(request_generator, save_token_silently):
    """Perform common authentication request functions."""
    try:
        jwt_token = request_generator()
        logger.info(f'JWT Token: {jwt_token}')

        save_message = 'Store token for future use (overwrites existing)?'
        if save_token_silently or click.confirm(save_message):
            config.set_token(jwt_token)
    except HTTPError as http_error:
        logger.error(f'There was an error with registration: {http_error}')


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option('-h', '--host', default=None)
@click.option('-y', '--save-token-silently', default=False)
@click.argument('username')
@click.argument('user_email')
@click.argument('password')
def register(host, save_token_silently, username, user_email, password):
    """Register as a new MetaGenScope user."""
    if host is None:
        host = os.environ['MGS_HOST']
    authenticator = Authenticator(host=host)

    def request_generator():
        """Generate registration auth request."""
        return authenticator.register(username, user_email, password)

    handle_auth_request(request_generator, save_token_silently)


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option('-h', '--host', default=None)
@click.option('-y', '--save-token-silently', default=False)
@click.argument('user_email')
@click.argument('password')
def login(host, save_token_silently, user_email, password):
    """Authenticate as an existing MetaGenScope user."""
    if host is None:
        host = os.environ['MGS_HOST']
    authenticator = Authenticator(host=host)

    def request_generator():
        """Generate registration auth request."""
        return authenticator.login(user_email, password)

    handle_auth_request(request_generator, save_token_silently)


@click.command()
@click_log.simple_verbosity_option(logger)
@add_authorization()
def status(uploader):
    """Get user status."""
    response = uploader.knex.get('/api/v1/auth/status')
    logger.info(response)
