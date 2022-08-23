"""Test io/readers.py."""

from typing import List

from graphinder.io.readers import read_domains
from graphinder.pool.domain import Domain
from graphinder.utils.logger import setup_logger


def test_read_domains_input_domain() -> None:
    """read_domains test with input domain."""

    out: List[Domain] = read_domains(None, 'example.com')

    assert len(out) == 1
    assert out[0].url == 'example.com'


def test_read_domains_wrong_input_file() -> None:
    """read_domains test with wrong input file."""

    try:
        _: List[Domain] = read_domains(None, None)
    except AttributeError:
        pass


def test_read_domains_input_file() -> None:
    """read_domains test with input file."""

    setup_logger(False)

    with open('tests/unit/io/test_readers.txt', 'r', encoding='utf-8') as input_file:
        out: List[Domain] = read_domains(input_file, None)

    str_out = set(domain.url for domain in out)

    assert {'example.com', 'example.org', 'example.fr'} == str_out
