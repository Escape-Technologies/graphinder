"""Test entities/errors.py."""

from asyncio.exceptions import TimeoutError as AsyncioTimeoutError
from socket import gaierror

from aiohttp.client_exceptions import ClientError

from graphinder.entities.errors import AwaitableRequestException


def test_awaitable_exception_type() -> None:
    """Test AwaitableRequestException type."""

    assert len(AwaitableRequestException) == 4

    assert ClientError in AwaitableRequestException
    assert AsyncioTimeoutError in AwaitableRequestException
    assert gaierror in AwaitableRequestException
    assert UnicodeError in AwaitableRequestException
