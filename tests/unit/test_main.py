"""unit tests."""

from graphinder import __version__


def test_version() -> None:
    """Version Test."""
    assert __version__ == '1.0.0-beta.0'
