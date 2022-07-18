"""All functions for detection."""

import re
from json import JSONDecodeError

import aiohttp

from graphinder.io.providers import gql_endpoints_characterizer

PAYLOAD: dict[str, str] = {'query': 'query {  __typename }'}


def _look_like_graphql_url(url: str) -> tuple[bool, str | None]:
    """Check if the url looks like a GraphQL endpoint."""

    for part in gql_endpoints_characterizer():
        if part in url:
            return True, part

    return False, None


async def _looks_different_than_closest_route(
    session: aiohttp.ClientSession,
    url: str,
    original_body: str,
) -> bool:
    """Check if a close route to the same endpoint is different than the original one."""

    look_likes, characterizer = _look_like_graphql_url(url)
    if look_likes and characterizer:

        random_url = url.replace(characterizer, 'random')
        async with session.post(random_url, json=PAYLOAD, timeout=10) as random_resp:
            random_text_body = await random_resp.text()

            if random_text_body != original_body:
                return True

    return False


async def looks_like_graphql_url(
    session: aiohttp.ClientSession,
    url: str,
) -> bool:
    """Check if the supplies url looks like a graphql endpoint."""

    text_body = None
    try:
        async with session.post(url, json=PAYLOAD, timeout=10) as resp:

            text_body = await resp.text()
            json_body = await resp.json()

            if json_body.get('data', {}).get('__typename') or json_body.get('errors', [{}])[0].get('message'):
                return True

            if await _looks_different_than_closest_route(session, url, text_body):
                return True

            if json_body.get('message') and '404' not in text_body and not re.search(r'not.found', text_body, re.IGNORECASE):
                return True

            return False
    except Exception as e:
        if isinstance(e, JSONDecodeError) and text_body:
            return await _looks_different_than_closest_route(session, url, text_body)

        return False


async def is_gql_endpoint(
    session: aiohttp.ClientSession,
    url: str,
) -> bool:
    """Check if the supplies url is a GQL endpoint."""

    try:
        # Check if the endpoint is similar to graphQL
        async with session.post(url, timeout=10) as request:
            response: dict = await request.json()
            _ = response['data']['__typename']

        return False

    except Exception:
        return await looks_like_graphql_url(session, url)
