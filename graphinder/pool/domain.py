"""Domain class."""

import os

import aiohttp

from graphinder.entities.pool import Url
from graphinder.pool.detectors import is_gql_endpoint
from graphinder.pool.extractors import extract_script_urls_from_page, extract_urls_from_script
from graphinder.utils.logger import get_logger


class Domain:

    """Domain entity."""

    def __init__(self, url: str) -> None:
        """Init domain."""

        self.url = url
        self.logger = get_logger(self.url)
        self.subdomains: list[str] = []

        self.results: set[Url] = set()

    def fetch_subdomains(self, reduce: int = 100) -> None:
        """Fetch subdomains."""

        self.logger.info('fetching subdomains...')

        _finder = os.popen(f'./subfinder -d {self.url} -silent -timeout 5')

        self.subdomains = _finder.read().split('\n')

        self.logger.info(f'found { len(self.subdomains) } subdomains.')
        if len(self.subdomains) > reduce:
            self.logger.debug('reducing the number of subdomains.')
            self.subdomains = self.subdomains[:reduce]

    async def fetch_script(self, session: aiohttp.ClientSession, url: str) -> set[Url]:
        """Fetch script for endpoints."""

        self.logger.debug(f'fetching script {url}...')

        return await extract_urls_from_script(session, url)

    async def fetch_page_scripts(self, session: aiohttp.ClientSession, url: str) -> set[Url]:
        """Fetch page for scripts url."""

        self.logger.debug(f'fetching page scripts {url}...')

        return await extract_script_urls_from_page(session, url)

    async def fetch_endpoint(self, session: aiohttp.ClientSession, url: str) -> None:
        """Fetch endpoint and determinate if this is a GQL endpoint."""

        self.logger.debug(f'fetching endpoint {url}...')

        if await is_gql_endpoint(session, url):

            self.logger.success(f'found GQL endpoint {url}.')
            self.results.add(Url(url))
