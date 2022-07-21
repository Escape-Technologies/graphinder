"""Test io/providers.py."""

from graphinder.io.providers import gql_endpoints_characterizer


def test_gql_endpoints_characterizer() -> None:
    """gql_endpoints_characterizer test."""

    endpoints = gql_endpoints_characterizer()

    assert len(endpoints) == len(set(endpoints)), 'There should be no duplicates.'
    assert len(endpoints) == (23*3) - 4, 'There should be no more endpoints. Please update the test if you added more.'
