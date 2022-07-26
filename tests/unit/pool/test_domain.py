"""Test pool/domain.py."""

from typing import Set

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
    domain.session = aiohttp.ClientSession()

    fetch_assets()

    domain.fetch_subdomains()
    assert len(domain.subdomains) == 100, 'There should be max 100 subdomain.'

    assert await domain.fetch_script('https://example.com') == set()
    await domain.session.close()
    assert domain.session.closed


@pytest.mark.asyncio
async def test_domain_class_2() -> None:
    """More domain class test."""

    setup_logger(False)
    domain: Domain = Domain('example2.com')
    domain.session = aiohttp.ClientSession()

    res: Set[Url] = await domain.fetch_script('https://cdn.jsdelivr.net/npm/graphql-playground-react/build/static/js/middleware.js')
    assert len(res) == 13

    res = await domain.fetch_page_scripts('https://gontoz.escape.tech/')
    assert len(res) == 0

    await domain.fetch_endpoint('https://gontoz.escape.tech/graphql')
    assert len(domain.results) == 1

    await domain.session.close()
    assert domain.session.closed
