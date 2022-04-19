"""Test io/printers.py."""

from typing import Any

from graphinder.entities.io import Results
from graphinder.entities.pool import Url
from graphinder.io.printers import display_results


def test_display_results(capsys: Any) -> None:
    """display_results test."""

    results: Results = {
        'example.com': {Url('http://example.com/')},
        'example.org': {Url('http://example.org/')},
    }
    display_results(results)

    assert capsys.readouterr().out == 'example.com - 1\n\thttp://example.com/\nexample.org - 1\n\thttp://example.org/\n'
