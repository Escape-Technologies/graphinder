"""Scan functions."""

from time import sleep

import click
import progressbar  # type:ignore
import sublist3r  # type:ignore
from colorama import Fore  # type: ignore
from loguru import logger
from playwright.sync_api import sync_playwright

from graphinder.extractors import extract_from_scripts, network_extract_endpoint


def handle_domain_name(domain: str, verbose: bool, scripts: bool, subdomains: bool, subdomains_bruteforce: bool, output_file: click.Path | None) -> None:
    """extracts the GQL endpoint from the domain name provided."""

    endpoints = []

    if subdomains or subdomains_bruteforce:
        # Find all the subdomains for the given domain
        sbdomains = sublist3r.main(
            domain, 40, savefile=None, ports=None, silent=not verbose, verbose=verbose, enable_bruteforce=subdomains_bruteforce, engines=None
        )
    else:
        sbdomains = [domain]

    logger.info('Extracting GraphQL calls')

    with sync_playwright() as p:
        for subdomain in sbdomains:
            endpoints += network_extract_endpoint(subdomain, p)
            sleep(0.1)

    if scripts:
        logger.info('Extracting GraphQL endpoints from scripts found on page')
        for subdomain in sbdomains:
            detected_endpoint = extract_from_scripts(subdomain)
            logger.info(f'Scan of {subdomain} finished')
            if detected_endpoint:
                logger.info(f'Detected: {detected_endpoint}')
            endpoints += detected_endpoint

    endpoints = list(set(endpoints))

    for endpoint in endpoints:
        if verbose:
            logger.success(f'GraphQL endpoint Detected: {endpoint}')
        else:
            print(Fore.GREEN + 'GraphQL endpoint Detected:', end=' ')
            print(Fore.WHITE + endpoint)

    if output_file is not None:
        with open(output_file, 'a', encoding='utf-8') as f:  #type:ignore
            for item in endpoints:
                f.write(f'{item}\n')


def handle_domain_file(file: click.File, verbose: bool, scripts: bool, subdomains: bool, subdomains_bruteforce: bool, output_file: click.Path | None) -> None:
    """extracts the GQL endpoint from the domain names in the text file provided."""
    domains = file.readlines()  #type: ignore

    widgets = [
        progressbar.Bar('▆'),
        ' (',
        progressbar.ETA(),
        ') ',
    ]

    bar_prog = progressbar.ProgressBar(maxval=len(domains), widgets=widgets).start()

    for i, line in enumerate(bar_prog(domains)):
        domain = line.strip()
        handle_domain_name(domain, verbose, scripts, subdomains, subdomains_bruteforce, output_file)
        sleep(0.5)
        bar_prog.update(i)
