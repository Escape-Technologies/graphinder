"""Test utils/filters.py."""

from graphinder.entities.pool import Url
from graphinder.io.providers import gql_endpoints_characterizer
from graphinder.utils.filters import filter_common, filter_urls


def test_filter_common() -> None:
    """test for filter_common."""

    _input: set[str] = {
        'https://w3.org',
        'https://localhost',
        'https://schema.org',
        'https://sentry.io',
        'https://git.io',
        'https://github.com',
        'https://nuxtjs.org',
        'https://momentjs.com',
        'https://fb.me',
        'https://reactjs.org',
        'https://slack',
        'https://google',
        'https://twitter',
        'https://example.com',
        'https://apps.example.com',
        'https://www.example.com',
        'https://example.com/graphql',
        'https://example.com/api/graphql',
        'https://example.com/api/v1/graphql',
        'https://example.com/graphql',
        'https://example.com/api/graphql',
        'https://example.com/api/v1/graphql',
    }

    assert filter_common(_input) == {
        'https://example.com', 'https://apps.example.com', 'https://www.example.com', 'https://example.com/graphql', 'https://example.com/api/graphql',
        'https://example.com/api/v1/graphql', 'https://example.com/graphql', 'https://example.com/api/graphql', 'https://example.com/api/v1/graphql'
    }


def test_filter_urls() -> None:
    """test for filter_urls."""

    _input: set[Url] = set()

    for url in gql_endpoints_characterizer():
        _input.add(Url('https://example.com/' + url))

    assert filter_urls(_input) == {
        Url('https://example.com/v1/graphql/schema.json'),
        Url('https://example.com/v1/graphql/schema.yaml'),
        Url('https://example.com/v1/graphiql.min.css'),
        Url('https://example.com/v1/graphql-explorer'),
        Url('https://example.com/v2/graphiql.min.css'),
        Url('https://example.com/v2/graphql/schema.json'),
        Url('https://example.com/v2/graphql-explorer'),
        Url('https://example.com/graphql/schema.yaml'),
        Url('https://example.com/graphiql.min.css'),
        Url('https://example.com/v2/graphql/schema.yaml'),
        Url('https://example.com/graphql-explorer'),
        Url('https://example.com/graphql/schema.json'),
    }
