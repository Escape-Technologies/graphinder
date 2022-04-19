"""Test entities/io.py."""

from graphinder.entities.io import Results
from graphinder.entities.pool import Url


def test_results_type() -> None:
    """Test Results type."""

    r: Results = {'domain': set()}
    r['domain'].add(Url('https://example.com'))

    assert len(r) == 1
    assert len(r['domain']) == 1
