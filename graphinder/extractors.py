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

DIR_LIST = [
    'altair', 'explorer', 'graphiql', 'graphiql.css', 'graphiql/finland', 'graphiql.js', 'graphiql.min.css', 'graphiql.min.js', 'graphiql.php', 'graphql',
    'graphql-explorer', 'graphql.php', 'playground', 'subscriptions', 'api/graphql', 'graph', 'v1/altair', 'v1/explorer', 'v1/graphiql', 'v1/graphiql.css',
    'v1/graphiql/finland', 'v1/graphiql.js', 'v1/graphiql.min.css', 'v1/graphiql.min.js', 'v1/graphiql.php', 'v1/graphql', 'v1/graphql-explorer',
    'v1/graphql.php', 'v1/playground', 'v1/subscriptions', 'v1/api/graphql', 'v1/graph', 'v2/altair', 'v2/explorer', 'v2/graphiql', 'v2/graphiql.css',
    'v2/graphiql/finland', 'v2/graphiql.js', 'v2/graphiql.min.css', 'v2/graphiql.min.js', 'v2/graphiql.php', 'v2/graphql', 'v2/graphql.php', 'v2/playground',
    'v2/subscriptions', 'v2/api/graphql', 'v2/graph'
]


def network_extract_endpoint(url: str, p: Playwright) -> list:
    """"extracts the GQL endpoint if found in the requests the page made."""

    results: list = []

    def is_gql(response: str, request_data: str) -> bool:

        res_payloads = ['{\'data\':', '{"data":']
        req_payloads = ['"query"', 'query{', 'mutation{', 'subscription{']

        res_detection: bool = False
        req_detection: bool = False

        for payload in res_payloads:
            if payload in response.strip():
                res_detection = True

        for payload in req_payloads:
            if payload in request_data.strip():
                req_detection = True

        return req_detection and res_detection

    def handle_response(response: Any) -> None:
        try:
            response_text = response.text()

            if is_gql(response_text, response.request.post_data.lower()):
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

    return list(set(results))


def extract_from_scripts(domain: str) -> list:
    """This extractor will check all scripts on the page for GQL endpoints."""
    try:
        url = f'http://{domain}/'

        session = requests.Session()
        # set the User-agent as a regular browser
        session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'

        soup = BeautifulSoup(session.get(url, timeout=10).content, 'html.parser')

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
                    conf_file
                )
                urls = filter_common(urls)
                for urll in urls:
                    potential_gql = f'{urll.removesuffix("/graphql").rstrip("/")}/graphql'
                    if is_gql_endpoint(potential_gql):
                        return [potential_gql]

        return []
    except Exception:  #in case the fetched page is down
        return []


def brute_force_directories(url: str) -> list[str]:
    """given a url will brute force directories to check for GraphQL endpoints."""
    endpoints = []
    for directory in DIR_LIST:
        current_url = f'http://{url.removesuffix("/graphql").rstrip("/")}' + '/' + directory
        if is_gql_endpoint(current_url):
            endpoints.append(current_url)
    return endpoints
