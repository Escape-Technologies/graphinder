"""Test pool/detectors.py."""

import aiohttp
import pytest

from graphinder.pool.detectors import is_gql_characterizer, is_gql_endpoint, looks_like_graphql_url


def test_is_gql_characterizer() -> None:
    """is_gql_characterizer test."""

    assert not is_gql_characterizer('https://example.com')
    assert is_gql_characterizer('https://example.com/graphql')


@pytest.mark.asyncio
async def test_looks_like_graphql_url() -> None:
    """looks_like_graphql_url test."""

    async with aiohttp.ClientSession() as session:

        assert not await looks_like_graphql_url(session, 'https://example.com')
        assert await looks_like_graphql_url(session, 'https://gontoz.escape.tech')


@pytest.mark.asyncio
async def test_is_gql_endpoint() -> None:
    """is_gql_endpoint test."""

    async with aiohttp.ClientSession() as session:

        assert not await is_gql_endpoint(session, 'https://example.com')
        assert await is_gql_endpoint(session, 'https://gontoz.escape.tech')
