"""The CLI."""

import argparse
import importlib.metadata
import logging
import sys
from datetime import date
from multiprocessing import cpu_count

from graphinder.entities.io import Results
from graphinder.pool import main_routine
from graphinder.utils.assets import fetch_assets
from graphinder.utils.logger import setup_logger

__version__ = importlib.metadata.version(__package__ or __name__)


def argument_builder(args: list[str]) -> argparse.Namespace:
    """Builds the arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument('--domain', '-d', dest='domain', type=str, help='Domain to scan')
    parser.add_argument('--input-file', '-f', dest='input_file', type=argparse.FileType('r+'), help='The path to the text file of domains to scan')
    parser.add_argument(
        '--inplace',
        '-i',
        dest='inplace',
        type=bool,
        help='Write the results in the same file as the input file, comma separated (CSV)',
        default=False,
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument('--output-file', '-o', dest='output_file', type=argparse.FileType('w'), help='The path of the results file', default='results.json')
    parser.add_argument('--verbose', '-v', dest='verbose_mode', type=bool, help='Verbose', default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument(
        '--script', '-s', dest='script_mode', type=bool, help='Check scripts assets to extract GraphQL calls', default=True,
        action=argparse.BooleanOptionalAction
    )
    parser.add_argument('--quiet', '-q', dest='quiet_mode', type=bool, help='Quiet', default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument(
        '--bruteforce', '-b', dest='bruteforce_mode', type=bool, help='Scan directory looking for GraphQL endpoints', default=True,
        action=argparse.BooleanOptionalAction
    )
    parser.add_argument('--precision', '-p', dest='precision_mode', type=bool, help='Use precision mode', default=True, action=argparse.BooleanOptionalAction)
    parser.add_argument('--reduce', '-r', dest='reduce_mode', type=int, help='The maximum number of subdomains to scan.', default=100)
    parser.add_argument(
        '--max-workers', '-w', dest='max_workers', type=int, help='Maximum number of concurrent workers in multi-urls mode.',
        default=(max(1, int(cpu_count() / 2)))
    )
    parser.add_argument('--webhook_url', '-wb', dest='webhook_url', type=str, help='The webhook url to send results.', default=None)

    return parser.parse_args(args)


def validate_arguments(
    logger: logging.Logger,
    args: argparse.Namespace,
) -> bool:
    """Validates the arguments."""

    if args.domain and args.input_file:
        return False

    if args.inplace and not args.input_file:
        logger.error('--inplace requires and --input-file')
        return False

    if not args.domain and not args.input_file:
        logger.error('you must supply a domain or a input_file.')
        return False

    if not args.script_mode and not args.bruteforce_mode:
        logger.error('no scanning mode selected.')
        return False

    return True


# pylint: disable=trailing-whitespace
def cli() -> None:
    """Entry point of the CLI program."""

    print(
        r"""
        ____                 _     _           _           
    / ___|_ __ __ _ _ __ | |__ (_)_ __   __| | ___ _ __ 
    | |  _| '__/ _` | '_ \| '_ \| | '_ \ / _` |/ _ \ '__|
    | |_| | | | (_| | |_) | | | | | | | | (_| |  __/ |   
    \____|_|  \__,_| .__/|_| |_|_|_| |_|\__,_|\___|_|   
                    |_|                                  

    """
    )

    print('    Maintainer   https://escape.tech')
    print('    Blog         https://blog.escape.tech')
    print('    DockerHub    https://hub.docker.com/r/escapetech/graphinder')
    print('    Contribute   https://github.com/Escape-Technologies/graphinder')
    print('')
    print(f'   (c) 2021 - { date.today().year } Escape Technologies - Version: {__version__}')
    print('\n' * 2)

    main()


def main(
    argv: list[str] | None = None,
    logger: logging.Logger | None = None,
) -> Results:
    """Ignites arguments."""

    if argv is None:
        argv = sys.argv[1:]

    args: argparse.Namespace = argument_builder(argv)

    logger = setup_logger(
        verbose_mode=args.verbose_mode,
        quiet_mode=args.quiet_mode,
        logger=logger,
    )
    if not validate_arguments(logger, args):
        return {}

    fetch_assets()

    return main_routine(args)
