import os
from sys import stderr
import click
from requests.exceptions import HTTPError

from metagenscope_cli.network.authenticator import Authenticator
from metagenscope_cli.config import config

from .utils import add_authorization


@click.group()
def create():
    pass


@create.command(name='org')
@add_authorization()
@click.option('--private/--public', default=True)
@click.argument('group_name')
@click.argument('admin_email')
def create_org(uploader, private, group_name, admin_email):
    """Create a new organization."""
    payload = {
        'name': group_name,
        'admin_email': admin_email,
    }
    if private:
        payload['access_scheme'] = 'private'
    try:
        response = uploader.knex.post('/api/v1/organizations', payload)
        click.echo(response)
    except HTTPError as exc:
        print(f'{exc}', file=stderr)


@click.group()
def add():
    pass


@add.command(name='group-to-org')
@add_authorization()
@click.argument('group_name')
@click.argument('org_uuid')
def add_group_to_org(uploader, group_name, org_uuid):
    """Add a group to an organization."""
    response = uploader.knex.get(f'/api/v1/sample_groups/getid/{group_name}')
    group_uuid = response['data']['sample_group_uuid']
    payload = {'sample_group_uuid': group_uuid}
    try:
        response = uploader.knex.post(
            f'/api/v1/organizations/{org_uuid}/sample_groups',
            payload
        )
        click.echo(response)
    except HTTPError as exc:
        print(f'{exc}', file=stderr)


@add.command(name='user-to-org')
@add_authorization()
@click.argument('user_id')
@click.argument('org_uuid')
def add_user_to_org(uploader, user_id, org_uuid):
    """Add a group to an organization."""
    payload = {'user_id': user_id}
    try:
        response = uploader.knex.post(
            f'/api/v1/organizations/{org_uuid}/users',
            payload
        )
        click.echo(response)
    except HTTPError as exc:
        print(f'{exc}', file=stderr)

