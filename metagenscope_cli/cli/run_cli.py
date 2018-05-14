"""CLI to run commands on MGS server."""

import click
import click_log

from metagenscope_cli.extensions import logger

from .utils import add_authorization


@click.group()
def run():
    """Run actions on the server."""
    pass


@run.group()
def middleware():
    """Run middleware."""
    pass


@middleware.command(name='group')
@click_log.simple_verbosity_option(logger)
@add_authorization()
@click.argument('group_uuid')
def group_middleware(uploader, group_uuid):
    """Run middleware for a group."""
    response = uploader.knex.post(f'/api/v1/sample_groups/{group_uuid}/middleware', {})
    logger.info(response)


@middleware.command(name='sample')
@click_log.simple_verbosity_option(logger)
@add_authorization()
@click.argument('sample_name')
def sample_middleware(uploader, sample_name):
    """Run middleware for a sample."""
    response = uploader.knex.get(f'/api/v1/samples/getid/{sample_name}')
    sample_uuid = response['data']['sample_uuid']
    logger.info(f'{sample_name} :: {sample_uuid}')
    response = uploader.knex.post(f'/api/v1/samples/{sample_uuid}/middleware', {})
    logger.info(response)
