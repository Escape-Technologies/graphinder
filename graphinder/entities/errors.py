"""Errors entities."""

from asyncio.exceptions import TimeoutError as AsyncioTimeoutError
from socket import gaierror

from aiohttp.client_exceptions import ClientError

AwaitableRequestException: tuple = (
    ClientError,
    AsyncioTimeoutError,
    gaierror,
    UnicodeError,
)
