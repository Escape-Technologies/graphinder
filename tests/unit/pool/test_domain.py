"""Test pool/domain.py."""

import aiohttp
import pytest

from graphinder.entities.pool import Url
from graphinder.pool.domain import Domain
from graphinder.utils.assets import fetch_assets
from graphinder.utils.logger import setup_logger


@pytest.mark.asyncio
async def test_domain_class() -> None:
    """Domain class test."""

    setup_logger(False)

    domain: Domain = Domain('example.com')
    fetch_assets()

    domain.fetch_subdomains()
    assert len(domain.subdomains) == 100, 'There should be max 100 subdomain.'

    async with aiohttp.ClientSession() as session:

        assert await domain.fetch_script(session, 'https://example.com') == set()


@pytest.mark.asyncio
async def test_domain_class_2() -> None:
    """More domain class test."""

    setup_logger(False)
    domain: Domain = Domain('example2.com')

    async with aiohttp.ClientSession() as session:
        res: set[Url] = await domain.fetch_script(session, 'https://cdn.jsdelivr.net/npm/graphql-playground-react/build/static/js/middleware.js')
        assert len(res) == 13

        res = await domain.fetch_page_scripts(session, 'https://gontoz.escape.tech/')
        assert len(res) == 0

        await domain.fetch_endpoint(session, 'https://gontoz.escape.tech/graphql')
        assert len(domain.results) == 1
