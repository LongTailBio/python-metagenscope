"""Knex wraps MetaGenScope requests requiring authentication."""

import requests

from metagenscope_cli.constants import DEFAULT_HOST
from metagenscope_cli.extensions import logger


class Knex(object):
    """Knex wraps MetaGenScope requests requiring authentication."""

    def __init__(self, token_auth, host=None, headers=None):
        """Instantiate Knex instance."""
        self.auth = token_auth

        self.host = host
        if self.host is None:
            self.host = DEFAULT_HOST

        self.headers = headers
        if self.headers is None:
            self.headers = {'Accept': 'application/json'}

    def post(self, endpoint, payload):
        """Perform authenticated POST request."""
        url = self.host + endpoint
        if payload:
            response = requests.post(url,
                                     headers=self.headers,
                                     auth=self.auth,
                                     json=payload)
        else:
            response = requests.post(url, headers=self.headers, auth=self.auth)
        if response.status_code >= 400:
            logger.error(response.content)
        response.raise_for_status()
        return response.json()

    def get(self, endpoint):
        """Perform authenticated GET request."""
        url = self.host + endpoint
        response = requests.get(url,
                                headers=self.headers,
                                auth=self.auth)
        response.raise_for_status()
        return response.json()
