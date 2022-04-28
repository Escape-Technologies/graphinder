"""The CLI."""

import argparse
import logging
import sys
from multiprocessing import cpu_count

from graphinder.pool import main_routine
from graphinder.utils.assets import fetch_assets
from graphinder.utils.logger import setup_logger


def argument_builder(args: list[str]) -> argparse.Namespace:
    """Builds the arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument('--domain', '-d', dest='domain', type=str, help='Domain to scan')
    parser.add_argument('--input-file', '-f', dest='input_file', type=argparse.FileType('r'), help='The path to the text file of domains to scan')
    parser.add_argument('--output-file', '-o', dest='output_file', type=argparse.FileType('w'), help='The path of the results file', default='results.txt')
    parser.add_argument('--verbose', '-v', dest='verbose_mode', type=bool, help='Verbose', default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument(
        '--script', '-s', dest='script_mode', type=bool, help='Check scripts assets to extract GraphQL calls', default=True,
        action=argparse.BooleanOptionalAction
    )
    parser.add_argument(
        '--bruteforce', '-b', dest='bruteforce_mode', type=bool, help='Scan directory looking for GraphQL endpoints', default=True,
        action=argparse.BooleanOptionalAction
    )
    parser.add_argument('--reduce', '-r', dest='reduce_mode', type=int, help='The maximum number of subdomains to scan.', default=100)
    parser.add_argument(
        '--max-workers', '-w', dest='max_workers', type=int, help='Maximum number of concurrent workers in multi-urls mode.', default=(cpu_count() / 2)
    )
    return parser.parse_args(args)


def validate_arguments(logger: logging.Logger, args: argparse.Namespace) -> bool:
    """Validates the arguments."""

    if args.domain and args.input_file:
        return False

    if not args.domain and not args.input_file:
        logger.error('you must supply a domain or a input_file.')
        return False

    if not args.script_mode and not args.bruteforce_mode:
        logger.error('no scanning mode selected.')
        return False

    return True


def main() -> bool:
    """Ignites arguments."""

    args: argparse.Namespace = argument_builder(sys.argv[1:])

    logger = setup_logger(args.verbose_mode)
    if not validate_arguments(logger, args):
        return False

    fetch_assets()

    main_routine(args)
    return True