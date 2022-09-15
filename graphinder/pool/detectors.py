"""All functions for detection."""

import asyncio
import json
import logging
import re
from typing import Any, Coroutine, Dict, Optional, Tuple

import aiohttp

from graphinder.io.providers import gql_endpoints_characterizer


def _look_like_graphql_url(url: str) -> Tuple[bool, Optional[str]]:
    """Check if the url looks like a GraphQL endpoint."""

    for part in gql_endpoints_characterizer():
        if part in url:
            return True, part

    return False, None


def _replace_last_resource(url: str, resource: str) -> Optional[str]:
    """Replace the last resource in the url with the given resource."""

    # https://hello.com
    if url.count('/') <= 2:
        return None

    # https://hello.com
    if url.count('/') == 3 and url.endswith('/'):
        return None

    lst = url.split('/')
    if lst[-1] == '':
        # https://hello.com/aaa/
        del lst[-1]
        lst[-1] = resource
        return '/'.join(lst) + '/'

    # else # https://hello.com/aaa
    lst[-1] = resource

    return '/'.join(lst)


async def _looks_different_than_closest_route(
    session: aiohttp.ClientSession,
    url: str,
    original_body: str,
) -> bool:
    """Check if a close route to the same endpoint is different than the original one."""

    look_likes, characterizer = _look_like_graphql_url(url)
    if look_likes and characterizer:

        random_url = _replace_last_resource(url, 'random')
        if random_url is None:
            return False

        async with session.post(
            random_url,
            json={'query': 'query {  __typename }'},
            timeout=10,
        ) as random_resp:
            random_text_body = await random_resp.text()

            if random_text_body != original_body:
                return True

    return False


async def empty_post_request(
    session: aiohttp.ClientSession,
    url: str,
    timeout: int,
) -> bool:
    """Send empty post request.

    If the response contains a GraphQL like JSON body, this must be a honeypot.
    """

    try:
        async with session.post(url, timeout=timeout) as request:
            response = await request.json()
            _ = response['data']['__typename']

        return True

    except Exception:
        return False


async def analyze_schema(text_body: str) -> Tuple[bool, bool]:
    """Perform futher analysis of the schema request."""

    is_valid = 'introspection' in text_body
    return is_valid, is_valid


async def analyze_typename(
    # session: aiohttp.ClientSession,
    # url: str,
    text_body: str,
    json_body: Dict,
) -> Tuple[bool, bool]:
    """Perform futher analysis of the typename request."""

    error_messages = json_body.get('errors', [{}])
    if isinstance(error_messages, list) \
        and len(error_messages) > 0 \
        and isinstance(error_messages[0], dict) \
        and error_messages[0].get('message') is not None:
        # Handle hasura errors
        if 'query is not in any of the allowlists' in text_body.lower():
            return True, True

        return True, False

    # Handle looks_like
    # if (await _looks_different_than_closest_route(
    #     session,
    #     url,
    #     text_body,
    # )):
    #     return True, False

    # Handle not found pages
    if json_body.get('message') is not None and \
        '404' not in text_body and \
        not re.search(r'not.found', text_body, re.IGNORECASE):
        return True, False

    return False, False


# pylint: disable=too-few-public-methods
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
    ) -> Tuple[bool, Optional[str], Optional[dict]]:
        """Send a request to the url.

        Returns:
            bool: If the request was successful.
            Optional[str]: The text body.
            Optional[dict]: The json body.
        """

        try:
            async with self._session.post(
                self._url,
                json=payload,
                timeout=self._timeout,
            ) as req:
                text_body = await req.text()
                json_body = json.loads(text_body)

                if json_body.get('data', {}).get(matching_key) is not None:
                    return True, None, None

                return False, text_body, json_body

        except Exception as e:
            if self._logger:
                self._logger.debug(f'Error while sending request to {self._url}: {e}')

        return False, None, None

    async def detect(self) -> Tuple[bool, bool]:
        """Detect if the url is a GraphQL endpoint."""

        post_request_task: Coroutine[bool, Any, Any] = empty_post_request(
            self._session,
            self._url,
            self._timeout,
        )
        query_tasks = [
            self._send_request(
                '__typename',
                {'query': 'query { __typename }'},
            ),
            self._send_request(
                '__schema',
                {'query': 'query { __schema { queryType { name } } }'},
            ),
        ]

        # If post request worked, it means likely honey pot
        post_request_status = await post_request_task
        if post_request_status:
            return False, False

        for query in asyncio.as_completed(query_tasks):
            status, text_body, json_body = await query
            if status:
                self.valid_graphql = True
                self.valid_auth = True
                break

            if not text_body or not json_body:
                continue

            further_analysis = await analyze_typename(text_body, json_body) \
                if query_tasks[0] else await analyze_schema(text_body)
            if further_analysis[0]:
                self.valid_graphql = True
            if further_analysis[1]:
                self.valid_auth = True

        return self.valid_graphql, self.valid_auth


async def is_gql_endpoint(
    url: str,
    session: Optional[aiohttp.ClientSession] = None,
    headers: Optional[Dict] = None,
    logger: Optional[logging.Logger] = None,
) -> Tuple[bool, bool]:
    """Check if the given url seems to be GraphQL endpoint.

    Args:
        session: aiohttp session with auth headers
        url: url to check
        logger: logger to use

    Returns:
        bool: True if the url is a GraphQL endpoint, False otherwise.
        bool: True if the authentication is valid, False otherwise.
    """

    assert url, 'URL is required'

    headers = headers or {}

    # Open new session if necessary
    has_opened_new_session = False
    if not session:
        session = aiohttp.ClientSession(headers=headers)
        has_opened_new_session = True
    else:
        assert isinstance(session, aiohttp.ClientSession), 'Valid session must be provided'

    detector = GraphQLEndpointDetector(
        session,
        url,
        logger,
    )

    status = await detector.detect()

    if has_opened_new_session:
        if logger:
            logger.debug('Closing previously opened session')
        await session.close()

    return status
