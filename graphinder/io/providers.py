"""Provide datas to graphinder."""

import pkgutil


def gql_endpoints_characterizer() -> list[str]:
    """return list of most common GQL endpoints."""
    endpoints: bytes | None = pkgutil.get_data(__name__, 'gql_urls.txt')

    return [] if endpoints is None else endpoints.decode('utf-8').split('\n')
