"""Domain class."""

import asyncio
import os

import aiohttp

from graphinder.entities.pool import Url
from graphinder.pool.detectors import is_gql_endpoint
from graphinder.pool.extractors import extract_script_urls_from_page, extract_urls_from_script
from graphinder.utils.filters import remove_duplicate_domains
from graphinder.utils.logger import get_logger


class Domain:

    """Domain entity."""

    semaphore: asyncio.Semaphore | None
    session: aiohttp.ClientSession

    def __init__(
        self,
        url: str,
        precision_mode: bool = False,
    ) -> None:
        """Init domain."""

        self.url = url
        self.logger = get_logger()
        self.subdomains: list[str] = []

        if precision_mode:
            self.semaphore = asyncio.Semaphore(100)
        else:
            self.semaphore = None

        self.results: set[Url] = set()

    def fetch_subdomains(
        self,
        reduce: int = 100,
    ) -> None:
        """Fetch subdomains."""

        self.logger.info('fetching subdomains...')

        _finder = os.popen(f'./subfinder -d {self.url} -silent -timeout 5')

        self.subdomains = _finder.read().split('\n')

        self.subdomains = remove_duplicate_domains(self.subdomains)
        self.logger.info(f'{self.url} - found { len(self.subdomains) } subdomains.')

        if len(self.subdomains) > reduce:
            self.logger.debug('reducing the number of subdomains.')
            self.subdomains = self.subdomains[:reduce]

    async def fetch_script(
        self,
        url: str,
    ) -> set[Url]:
        """Fetch script for endpoints."""

        self.logger.debug(f'fetching script {url}...')

        return await extract_urls_from_script(self.session, url)

    async def fetch_page_scripts(
        self,
        url: str,
    ) -> set[Url]:
        """Fetch page for scripts url."""

        self.logger.debug(f'fetching page scripts {url}...')

        return await extract_script_urls_from_page(self.session, url)

    async def fetch_endpoint(
        self,
        url: str,
    ) -> None:
        """Fetch endpoint and determinate if this is a GQL endpoint."""

        self.logger.debug(f'fetching endpoint {url}...')

        if await is_gql_endpoint(self.session, url):
            self.logger.info(f'found GQL endpoint {url}.')
            self.results.add(Url(url))
