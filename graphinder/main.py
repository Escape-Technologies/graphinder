"""The CLI."""

import argparse
import asyncio
import logging
import sys
from datetime import date
from typing import List, Optional

import pkg_resources

from graphinder.entities.io import Results
from graphinder.pool import main_routine
from graphinder.utils.assets import fetch_assets
from graphinder.utils.logger import setup_logger

__version__ = pkg_resources.get_distribution(__package__ or __name__).version


def argument_builder(args: List[str]) -> argparse.Namespace:
    """Builds the arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--domain',
        '-d',
        dest='domain',
        type=str,
        help='Domain to scan',
    )
    parser.add_argument(
        '--output-file',
        '-o',
        dest='output_file',
        type=argparse.FileType('w'),
        help='The path of the results file',
        default='results.json',
    )
    parser.add_argument(
        '--verbose',
        '-v',
        dest='verbose_mode',
        type=bool,
        help='Verbose',
        default=False,
    )
    parser.add_argument(
        '--no-script',
        '-ns',
        dest='no_script_mode',
        help='Disable script scanning',
        action='store_true',
    )
    parser.add_argument(
        '--quiet',
        '-q',
        dest='quiet_mode',
        help='Quiet',
        action='store_true',
    )
    parser.add_argument(
        '--no-bruteforce',
        '-nb',
        dest='no_bruteforce_mode',
        help='Disable directory scanning',
        action='store_true',
    )
    parser.add_argument(
        '--precision',
        '-p',
        dest='precision_mode',
        type=bool,
        help='Use precision mode',
        default=True,
    )
    parser.add_argument(
        '--reduce',
        '-r',
        dest='reduce_mode',
        type=int,
        help='The maximum number of subdomains to scan.',
        default=100,
    )
    parser.add_argument(
        '--webhook_url',
        '-wb',
        dest='webhook_url',
        type=str,
        help='The webhook url to send results.',
        default=None,
    )

    return parser.parse_args(args)


def validate_arguments(
    logger: logging.Logger,
    args: argparse.Namespace,
) -> bool:
    """Validates the arguments."""

    if args.domain is None:
        logger.error('no domain provided')
        return False

    if args.no_script_mode and args.no_bruteforce_mode:
        logger.error('no scanning mode selected.')
        return False

    if args.precision_mode:
        logger.info('precision mode enabled')

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


async def async_main(
    argv: Optional[List[str]] = None,
    logger: Optional[logging.Logger] = None,
) -> Results:
    """Async main."""

    return await loop(argv, logger)


def main(
    argv: Optional[List[str]] = None,
    logger: Optional[logging.Logger] = None,
) -> Results:
    """Main."""

    return asyncio.run(loop(argv, logger))


async def loop(
    argv: Optional[List[str]] = None,
    logger: Optional[logging.Logger] = None,
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
    return await main_routine(args)
