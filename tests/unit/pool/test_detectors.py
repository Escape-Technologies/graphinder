"""Test pool/detectors.py."""

import aiohttp
import pytest

from graphinder.pool.detectors import _look_like_graphql_url, is_gql_endpoint, looks_like_graphql_url


def test_look_like_graphql_url() -> None:
    """_look_like_graphql_url test."""

    assert _look_like_graphql_url('https://example.com') == (False, None)
    assert _look_like_graphql_url('https://example.com/graphql') == (True, 'graphql')


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
