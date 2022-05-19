"""Test utils/filters.py."""

import pytest

from graphinder.entities.pool import Url
from graphinder.io.providers import gql_endpoints_characterizer
from graphinder.utils.filters import filter_common, filter_urls, remove_duplicate_domains, transform_url_in_domain


def test_filter_common() -> None:
    """test for filter_common."""

    _input: set[str] = {
        'http://a',
        'http://x',
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

    assert filter_urls(_input) == {Url('https://example.com/graphql')}


def test_remove_duplicate_domains() -> None:
    """test for duplicate_domain."""

    domains: list[str] = [
        'example.com',
        'www.example.com',
    ]

    assert remove_duplicate_domains(domains) == [
        'example.com',
    ]


@pytest.mark.parametrize('url,expected', [
    ('https://example.com', 'example.com'),
    ('https://example.com/', 'example.com'),
])
def test_transform_url_in_domain(url: str, expected: str) -> None:
    """test for transform_url_in_domain."""

    assert transform_url_in_domain(url) == expected
