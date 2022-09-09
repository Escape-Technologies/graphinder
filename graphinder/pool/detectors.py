"""All functions for detection."""

import asyncio
import json
import logging
import re
from json import JSONDecodeError
from typing import Any, Coroutine, Dict, Optional, Tuple

import aiohttp

from graphinder.io.providers import gql_endpoints_characterizer

PAYLOAD: Dict[str, str] = {'query': 'query {  __typename }'}


def _look_like_graphql_url(url: str) -> Tuple[bool, Optional[str]]:
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


# async def is_gql_endpoint(
#     session: aiohttp.ClientSession,
#     url: str,
# ) -> bool:
#     """Check if the supplies url is a GQL endpoint."""

#     try:
#         # Check if the endpoint is similar to graphQL
#         async with session.post(url, timeout=10) as request:
#             response: dict = await request.json()
#             _ = response['data']['__typename']

#         return False

#     except Exception:
#         return await looks_like_graphql_url(session, url)


async def empty_post_request(
    session: aiohttp.ClientSession,
    url: str,
    timeout: int,
) -> bool:
    """Send empty post request."""

    try:
        async with session.post(url, timeout=timeout) as request:
            response = await request.json()
            _ = response['data']['__typename']

        return True

    except (JSONDecodeError, KeyError):
        return False


class GraphQLEndpointDetector:

    """Check if the url is a valid GraphQL endpoint."""

    valid_auth: bool = False
    valid_graphql: bool = False

    _session: aiohttp.ClientSession
    _url: str
    _timeout: int
    _logger: Optional[logging.Logger]

    def __init__(
        self,
        session: aiohttp.ClientSession,
        url: str,
        logger: Optional[logging.Logger] = None,
        timeout: int = 10,
    ) -> None:
        """Initialize the detector."""

        self._session = session
        self._url = url
        self._timeout = timeout
        self._logger = logger

        session.headers.update({'Content-Type': 'application/json'})

    async def _send_request(
        self,
        matching_key: str,
        payload: Optional[Dict],
    ) -> Tuple[bool, bool, Optional[aiohttp.ClientResponse]]:
        """Send a request to the url."""

        try:
            async with self._session.post(self._url, json=payload, timeout=self._timeout) as _req:
                text_body = await _req.text()
                json_body = json.loads(text_body)
                if json_body.get('data', {}).get(matching_key) is not None:
                    return True, True, _req

        except Exception as e:
            if self._logger:
                self._logger.debug(f'Error while sending request to {self._url}: {e}')

        return False, False, None

    async def detect(self) -> Tuple[bool, bool]:
        """Detect if the url is a GraphQL endpoint."""

        post_request_task: Coroutine[bool, Any, Any] = empty_post_request(
            self._session,
            self._url,
            self._timeout,
        )
        query_tasks = [
            self._send_request('__typename', {'query': 'query { __typename }'}),
            self._send_request('__schema', {'query': 'query { __schema { queryType { name } } }'}),
        ]

        # If post request worked, it means likely honey pot
        post_request_status = await post_request_task
        if post_request_status:
            return False, False

        for query in asyncio.as_completed(query_tasks):
            pass

        return self.valid_graphql, self.valid_auth


async def is_gql_endpoint(
    session: aiohttp.ClientSession,
    url: str,
    logger: Optional[logging.Logger] = None,
) -> Tuple[bool, bool]:
    """Check if the given url seems to be GraphQL endpoint.

    Args:
        session: aiohttp session
        url: url to check
        logger: logger to use

    Returns:
        bool: True if the url is a GraphQL endpoint, False otherwise.
        bool: True if the authentication is valid, False otherwise.
    """

    return await (GraphQLEndpointDetector(session, url, logger=logger).detect())
