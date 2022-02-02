"""Scan functions."""

import json
from time import sleep

import click
import progressbar  # type:ignore
import sublist3r  # type:ignore
from colorama import Fore  # type: ignore
from loguru import logger
from playwright.sync_api import sync_playwright

from graphinder.extractors import brute_force_directories, extract_from_scripts, network_extract_endpoint
from graphinder.utils import format_dict, reduce_domains, remove_duplicate_domains


def handle_domain_name( #pylint: disable=too-many-branches
    domain: str, verbose: bool, scripts: bool, subdomains: bool, subdomains_bruteforce: bool, directory_bruteforce: bool, output_file: click.Path | None, reduce:int, #pylint: disable=line-too-long
    return_dict: bool = False
) -> dict | None:
    """extracts the GQL endpoint from the domain name provided."""

    if subdomains or subdomains_bruteforce:
        # Find all the subdomains for the given domain
        sdomains = sublist3r.main(
            domain, 40, savefile=None, ports=None, silent=not verbose, verbose=verbose, enable_bruteforce=subdomains_bruteforce, engines=None
        )
        sbdomains = remove_duplicate_domains(sdomains)
        if reduce is not None:
            if len(sbdomains) > reduce:
                logger.info('reducing the number of subdomains')
                sbdomains = reduce_domains(sbdomains)
    else:
        sbdomains = [domain]

    dict_sbdomains = format_dict(sbdomains)

    logger.info('Extracting GraphQL calls')

    with sync_playwright() as p:
        for subdomain, endpoints in dict_sbdomains.items():
            endpoints += network_extract_endpoint(subdomain, p)
            sleep(0.1)
            if endpoints:
                logger.info(f'Detected: {endpoints}')

    if scripts:
        logger.info('Extracting GraphQL endpoints from scripts found on page')
        for subdomain, endpoints in dict_sbdomains.items():
            detected_endpoint = extract_from_scripts(subdomain)
            logger.info(f'Scan of {subdomain} finished')
            if detected_endpoint:
                logger.info(f'Detected: {detected_endpoint}')
            endpoints += detected_endpoint
            endpoints = list(set(endpoints))

    if directory_bruteforce:
        logger.info('Bruteforcing Directories')
        for subdomain, endpoints in dict_sbdomains.items():
            logger.info(f'Bruteforcing {subdomain}')
            endpoints += brute_force_directories(subdomain)

    for endpoints in dict_sbdomains.values():
        if endpoints:
            for endpoint in endpoints:
                if verbose:
                    logger.success(f'GraphQL endpoint Detected: {endpoint}')
                else:
                    print(Fore.GREEN + 'GraphQL endpoint Detected:', end=' ')
                    print(Fore.WHITE + endpoint)

    if output_file is not None and not return_dict:
        with open(output_file, 'w', encoding='utf-8') as f:  #type:ignore
            json.dump({domain: dict_sbdomains}, f)

    if return_dict:
        return dict_sbdomains

    return None


def handle_domain_file(
    file: click.File, verbose: bool, scripts: bool, subdomains: bool, subdomains_bruteforce: bool, directory_bruteforce: bool, output_file: click.Path | None,
    reduce: int
) -> None:
    """extracts the GQL endpoint from the domain names in the text file provided."""
    domains = file.readlines()  #type: ignore

    widgets = [
        progressbar.Bar('▆'),
        progressbar.Percentage(),
        ' (',
        progressbar.ETA(),
        ') ',
    ]

    bar_prog = progressbar.ProgressBar(maxval=len(domains), widgets=widgets).start()

    results = []

    for i, line in enumerate(bar_prog(domains)):
        domain = line.strip()
        results.append({
            domain:
                handle_domain_name(domain, verbose, scripts, subdomains, subdomains_bruteforce, directory_bruteforce, output_file, reduce, return_dict=True)
        })
        sleep(0.5)
        bar_prog.update(i)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:  #type:ignore
                json.dump(results, f)
