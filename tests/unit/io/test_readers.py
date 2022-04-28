"""Test io/readers.py."""

from graphinder.io.readers import read_domains
from graphinder.pool.domain import Domain
from graphinder.utils.logger import setup_logger


def test_read_domains_input_domain() -> None:
    """read_domains test with input domain."""

    out: list[Domain] = read_domains(None, 'example.com')

    assert len(out) == 1
    assert out[0].url == 'example.com'


def test_read_domains_wrong_input_file() -> None:
    """read_domains test with wrong input file."""

    try:
        _: list[Domain] = read_domains(None, None)
    except AttributeError:
        pass


def test_read_domains_input_file() -> None:
    """read_domains test with input file."""

    setup_logger(False)

    with open('tests/unit/io/test_readers.txt', 'r', encoding='utf-8') as input_file:
        out: list[Domain] = read_domains(input_file, None)  # type: ignore[arg-type]

    assert len(out) == 2

    assert 'example.com' in [domain.url for domain in out]
    assert 'example.org' in [domain.url for domain in out]
