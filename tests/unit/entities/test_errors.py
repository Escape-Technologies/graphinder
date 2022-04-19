"""Test entities/errors.py."""

from asyncio.exceptions import TimeoutError as AsyncioTimeoutError
from socket import gaierror

from aiohttp.client_exceptions import ClientConnectionError, ClientResponseError, TooManyRedirects

from graphinder.entities.errors import AwaitableRequestException


def test_awaitable_exception_type() -> None:
    """Test AwaitableRequestException type."""

    assert len(AwaitableRequestException) == 6

    assert ClientConnectionError in AwaitableRequestException
    assert TooManyRedirects in AwaitableRequestException
    assert ClientResponseError in AwaitableRequestException
    assert AsyncioTimeoutError in AwaitableRequestException
    assert gaierror in AwaitableRequestException
    assert UnicodeError in AwaitableRequestException
