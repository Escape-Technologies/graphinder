"""Unit tests for the util functions."""

from graphinder.utils import remove_duplicate_domains


def test_remove_duplicate_domains() -> None:
    """test for remove_duplicate_domains."""

    domains = ['example.com', 'apps.example.com', 'www.example.com', 'api.example.com', 'shop.example.com', 'www.shop.example.com']
    domain_no_duplicates = ['example.com', 'apps.example.com', 'api.example.com', 'shop.example.com']

    assert remove_duplicate_domains(domains) == domain_no_duplicates
