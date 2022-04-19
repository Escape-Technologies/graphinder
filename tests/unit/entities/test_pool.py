"""Test entities/pool.py."""

from graphinder.entities.pool import Url


def test_url_type() -> None:
    """Test Url type."""

    url: Url = Url('https://example.com')

    assert isinstance(url, str)
