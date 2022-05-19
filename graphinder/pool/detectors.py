"""All functions for detection."""

import re
from json import JSONDecodeError

import aiohttp

from graphinder.io.providers import gql_endpoints_characterizer


def is_gql_characterizer(url: str) -> bool:
    """Check if the url is characterized as GQL endpoint."""

    return any(x in url for x in gql_endpoints_characterizer())


async def looks_like_graphql_url(session: aiohttp.ClientSession, url: str) -> bool:
    """Check if the supplies url looks like a graphql endpoint."""

    _payload: dict[str, str] = {'query': 'query {\n  __typename\n}'}
    try:
        async with session.post(url, json=_payload, timeout=10) as gql_request:

            text: str = await gql_request.text()
            if text == 'GET query missing.':
                return True

            gql_response: dict = await gql_request.json()
            if gql_response.get('data', {}).get('__typename') or gql_response.get('errors', [{}])[0].get('message'):
                return True

            if gql_response.get('message') and is_gql_characterizer(url):
                if '404' not in text and not re.search(r'not.found', text, re.IGNORECASE):
                    return True

            return False

    except JSONDecodeError:
        return is_gql_characterizer(url)

    except Exception:
        return False


async def is_gql_endpoint(session: aiohttp.ClientSession, url: str) -> bool:
    """Check if the supplies url is a GQL endpoint."""

    try:
        # Check if the endpoint is similar to graphQL
        async with session.post(url, timeout=10) as request:
            response: dict = await request.json()
            _ = response['data']['__typename']

        return False

    except Exception:
        return await looks_like_graphql_url(session, url)
