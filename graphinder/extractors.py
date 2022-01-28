"""All GQL endpoint extractor functions."""

import re
from typing import Any
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup  # type: ignore
from loguru import logger
from playwright.sync_api import Playwright

from graphinder.detectors import is_gql_endpoint
from graphinder.utils import filter_common


def network_extract_endpoint(url: str, p: Playwright) -> list:
    """"extracts the GQL endpoint if found in the requests the page made."""

    results: list = []

    def is_gql(response: str) -> bool:

        payloads = ['{\'data\':', '{"data":']

        for payload in payloads:
            if payload in response.strip():
                return True
        return False

    def handle_response(response: Any) -> None:
        try:
            response_text = response.text()

            if is_gql(response_text):
                results.append(response.url)
        except Exception:
            pass

    browser = p.firefox.launch()

    try:
        url = f'http://{url}/'
        page = browser.new_page()
        page.on('response', handle_response)
        page.goto(url, wait_until='networkidle', timeout=10000)
        page.context.close()

    except Exception as e:
        logger.warning(f'Error: while fetching: {url}, Error: {e}')
        page.context.close()

    browser.close()

    return results


def extract_from_scripts(domain: str) -> list:
    """This extractor will check all scripts on the page for GQL endpoints."""
    try:
        url = f'http://{domain}/'

        session = requests.Session()
        # set the User-agent as a regular browser
        session.headers[
            'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'

        soup = BeautifulSoup(
            session.get(url, timeout=10).content, 'html.parser')

        # get the JavaScript files On the loaded page
        script_files = []
        for script in soup.find_all('script'):
            if script.attrs.get('src'):
                # if the tag has the attribute 'src'
                script_url = urljoin(url, script.attrs.get('src'))
                script_files.append(script_url)

        # fetching every script and extacting all the urls from it
        for script_url in script_files:
            if domain in script_url:
                conf_file = requests.get(script_url).text
                urls = re.findall(
                    'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',  #pylint: disable=anomalous-backslash-in-string
                    conf_file)
                urls = filter_common(urls)
                for urll in urls:
                    potential_gql = f'{urll.rstrip("/graphql")}/graphql'
                    if is_gql_endpoint(potential_gql):
                        return [potential_gql]
        return []
    except requests.exceptions.ConnectionError:  #in case the fetched page is down
        return []
