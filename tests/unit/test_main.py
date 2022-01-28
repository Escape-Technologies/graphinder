"""unit tests."""

from graphinder import __version__


def test_version() -> None:
    """Hello."""
    assert __version__ == '1.0.0-beta.0'
