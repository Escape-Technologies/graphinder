"""Errors entities."""

from asyncio import TimeoutError as AsyncioTimeoutError
from socket import gaierror

from aiohttp.client_exceptions import ClientError, ClientPayloadError

AwaitableRequestException: tuple = (
    ClientError,
    AsyncioTimeoutError,
    gaierror,
    UnicodeError,
    ValueError,
    ClientPayloadError,
)
