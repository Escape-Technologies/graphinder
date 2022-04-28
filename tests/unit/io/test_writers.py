"""Test io/writter.py."""

import json
import os

from graphinder.entities.io import Results
from graphinder.entities.pool import Url
from graphinder.io.writers import ResultEncoder, write_results


def test_write_results_no_input() -> None:
    """write_results test with no input."""

    results: Results = {}

    write_results(None, results)


def test_result_encoder() -> None:
    """ResultEncoder test with wrong structure."""

    r = ResultEncoder()

    r.default(set())

    try:
        r.default(list())
        assert False, 'ResultEncoder should raise an exception.'
    except NotImplementedError:
        pass


def test_write_results() -> None:
    """write_results test."""

    results: Results = {
        'example.com': {Url('http://example.com/')},
        'example.org': {Url('http://example.org/')},
    }

    with open('test_write_results.json', 'w', encoding='utf-8') as output_file:
        write_results(output_file, results)  # type: ignore[arg-type]

    with open('test_write_results.json', 'r', encoding='utf-8') as output_file:
        results_from_file = json.load(output_file)

    for result in results_from_file.copy():
        results_from_file[result] = set(results_from_file[result])

    assert results_from_file == results
    assert os.path.isfile('test_write_results.json')

    os.remove('test_write_results.json')
