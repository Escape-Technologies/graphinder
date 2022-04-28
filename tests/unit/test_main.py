"""Test main.py."""

import argparse
import sys
from multiprocessing import cpu_count

from graphinder import __version__
from graphinder.main import argument_builder, main, validate_arguments
from graphinder.utils.logger import get_logger


def test_version() -> None:
    """version test."""
    assert __version__ == '1.0.20', 'Version has been changed, please update the test.'


def test_argument_builder() -> None:
    """argument_builder test."""

    args: argparse.Namespace = argument_builder([])

    assert args.domain is None
    assert args.input_file is None
    assert not args.verbose_mode
    assert args.script_mode
    assert args.bruteforce_mode
    assert args.reduce_mode == 100
    assert args.max_workers == cpu_count() / 2

    args = argument_builder(['-d', 'example.com'])

    assert args.domain == 'example.com'

    args = argument_builder(['--no-bruteforce'])

    assert not args.bruteforce_mode


def test_validate_arguments() -> None:
    """validate_arguments test."""

    logger = get_logger('test_validate_arguments')
    args: argparse.Namespace = argument_builder([])

    assert not validate_arguments(logger, args)

    args = argument_builder(['-d', 'example.com'])
    assert validate_arguments(logger, args)

    args = argument_builder(['--no-script', '--no-bruteforce'])
    assert not validate_arguments(logger, args)

    args = argument_builder(['-d', 'example.com', '--no-script', '--no-bruteforce'])
    assert not validate_arguments(logger, args)

    args = argument_builder(['-d', 'example.com', '-f', 'README.md'])
    assert not validate_arguments(logger, args)


def test_main() -> None:
    """main test."""
    sys.argv = ['graphinder']
    assert main() is False


def test_full_run() -> None:
    """Test a complete run."""

    sys.argv = ['graphinder', '-d', 'example.com']

    assert main() is True
