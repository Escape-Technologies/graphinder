"""All GQL endpoint extractor functions."""

from typing import List, Optional, Set
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup as bs4  # type: ignore[import]

from graphinder.entities.errors import AwaitableRequestException
from graphinder.entities.pool import Url
from graphinder.utils.filters import filter_common, remove_suffix
from graphinder.utils.finders import find_script_fetch_graphql, find_script_full_urls, find_script_window_base_urls


def extract_scripts_from_html(
    url: str,
    html: str,
) -> List[str]:
    """Get any scripts files from html page."""

    soup = bs4(html, 'html.parser')

    scripts_files = []
    for script in soup.find_all('script'):

        src: Optional[str] = script.attrs.get('src')

        if src:
            script_url = urljoin(url, script.attrs.get('src'))
            scripts_files.append(script_url)

    return scripts_files


async def extract_script_urls_from_page(
    session: aiohttp.ClientSession,
    url: str,
) -> Set[Url]:
    """This extractor will check all scripts on the page for GQL endpoints."""

    urls: Set[Url] = set()

    try:
        async with session.get(url, timeout=10) as page:
            _html: str = await page.text()
            _script_urls = extract_scripts_from_html(url, _html)

            for script_url in _script_urls:
                if url not in script_url:
                    continue

                urls.add(Url(script_url))

    except AwaitableRequestException:
        pass

    return urls


def extract_scripts_from_raw_js(
    url: str,
    script_file: str,
) -> Set[str]:
    """Extract all urls from a script file by using combination of regex."""

    urls: List[str] = find_script_full_urls(script_file) + find_script_window_base_urls(url, script_file) + find_script_fetch_graphql(url, script_file)

    return filter_common(set(urls))


async def extract_urls_from_script(
    session: aiohttp.ClientSession,
    url: str,
) -> Set[Url]:
    """Extract urls from scripts."""

    potentials_gqls: Set[Url] = set()
    if not url.endswith('.js'):
        return set()

    try:
        domain_url: str = '/'.join(url.split('/')[:3])
        async with session.get(url, timeout=10) as script:
            _content: str = await script.text()

            _urls: Set[str] = extract_scripts_from_raw_js(domain_url, _content)

            for potential in _urls:
                if not potential.endswith('/graphql') or not domain_url in potential:
                    potential = f'{remove_suffix(potential, "/graphql")}/graphql'

                potentials_gqls.add(Url(potential))

    except AwaitableRequestException:
        pass

    return potentials_gqls
