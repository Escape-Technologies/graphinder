"""The CLI."""
import sys

import click
from colorama import Fore  # type:ignore
from loguru import logger

from graphinder.scanner import handle_domain_file, handle_domain_name


@click.command()
@click.option('--domain', '-u', type=str, help='The subdomain to scan')
@click.option('--file', '-f', type=click.File(mode='r'), help='The path to the text file of subdomains to scan')
@click.option('--verbose', '-v', is_flag=True, help='verbose', default=False)
@click.option('--scripts', '-s', is_flag=True, help='check the scripts on a page for graphql calls', default=False)
@click.option('--network_calls', '-n', is_flag=True, help='check the network calls on a page for graphql endpoints', default=False)
@click.option('--reduce', '-r', type=int, help='The threshold that determines when to reduce subdomains')
@click.option('--subdomains', '-d', is_flag=True, help='check for all the subdomains that could be detected for the supplied domain', default=False)
@click.option('--subdomains_bruteforce', '-b', is_flag=True, help='detected subdomains via bruteforce (less recomended)', default=False)
@click.option('--directory_bruteforce', '-g', is_flag=True, help='Detected GraphQL via bruteforcing directories', default=False)
@click.option('--output_file', '-o', type=click.Path())
def finder(
    domain: str | None, file: click.File | None, verbose: bool, network_calls: bool, scripts: bool, subdomains: bool, subdomains_bruteforce: bool,
    output_file: click.Path | None, directory_bruteforce: bool, reduce: int
) -> None:
    """Find the all GraphQL endpoints from a given domain/domains list."""

    if not verbose:
        logger.remove()
        logger.add(sys.stderr, format='<lvl>{message}</lvl>', level='ERROR')

    if domain is not None and file is not None:
        click.ClickException('Two domain name sources were provided. Only one is needed.')

    if not network_calls and not scripts and not directory_bruteforce:
        if verbose:
            logger.critical('No scanning Mode Selected:\n Exiting.....')
            return None
        print(Fore.RED + 'No scanning Mode Selected:\n Exiting.....')
        return None

    if domain is not None:
        handle_domain_name(domain, verbose, network_calls, scripts, subdomains, subdomains_bruteforce, directory_bruteforce, output_file, reduce)
        return None

    if file is not None:
        handle_domain_file(file, verbose, network_calls, scripts, subdomains, subdomains_bruteforce, directory_bruteforce, output_file, reduce)
        return None

    click.ClickException('No domain source was provided')
    return None
