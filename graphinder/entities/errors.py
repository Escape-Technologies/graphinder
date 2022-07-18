"""Errors entities."""

from asyncio.exceptions import TimeoutError as AsyncioTimeoutError
from socket import gaierror

from aiohttp.client_exceptions import ClientConnectionError, ClientPayloadError, ClientResponseError, TooManyRedirects

AwaitableRequestException: tuple = (
    ClientConnectionError,
    ClientResponseError,
    TooManyRedirects,
    AsyncioTimeoutError,
    gaierror,
    UnicodeError,
    ClientPayloadError,
)
