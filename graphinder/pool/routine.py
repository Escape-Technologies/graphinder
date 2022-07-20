"""Functions to manage pooling."""

import argparse
import asyncio
import concurrent
from copy import deepcopy
from multiprocessing import Manager
from typing import cast

from graphinder.entities.io import Results
from graphinder.entities.tasks import TasksList
from graphinder.io.printers import display_results
from graphinder.io.readers import read_domains
from graphinder.io.writers import write_results, write_results_inplace
from graphinder.pool.domain import Domain, Url
from graphinder.pool.tasks import consume_tasks, init_domain_tasks
from graphinder.utils.filters import filter_urls
from graphinder.utils.logger import get_logger
from graphinder.utils.webhook import send_webhook


def domain_routine(
    domain: Domain,
    args: argparse.Namespace,
) -> dict[str, str | set[Url]]:
    """Start domain routine."""

    _tasks: TasksList = init_domain_tasks(domain, args)
    _urls: set[Url] = asyncio.run(consume_tasks(_tasks, domain))

    return {'domain': domain.url, 'urls': filter_urls(_urls)}


def process_pool(
    domains: list[Domain],
    args: argparse.Namespace,
    results: Results,
) -> None:
    """Manage graphinder pooling."""

    logger = get_logger()

    with concurrent.futures.ProcessPoolExecutor(max_workers=args.max_workers) as pool:
        promises = (pool.submit(domain_routine, domain, args) for domain in domains)

        for promise in concurrent.futures.as_completed(promises):
            result = promise.result()

            domain = cast(str, result['domain'])
            results[domain] = cast(set[Url], result['urls'])
            logger.info(f'{domain} has been scanned completly.')


def main_routine(args: argparse.Namespace) -> Results:
    """Main pool routine."""

    logger = get_logger()
    logger.info('starting main routine..')

    domains: list[Domain] = read_domains(args.input_file, args.domain, args.precision_mode)
    logger.info(f'{len(domains)} domains loaded.')

    args.max_workers = min(args.max_workers, len(domains))

    output_file = args.output_file
    input_file = args.input_file
    del args.output_file
    del args.input_file

    exported_results: Results = {}

    with Manager() as manager:

        results: Results = manager.dict()
        for domain in domains:
            results[domain.url] = manager.list()

        process_pool(domains, args, results)

        if not args.quiet_mode:
            display_results(results)

        if output_file is not None:
            write_results(output_file, results.copy())

        if args.inplace:
            write_results_inplace(input_file, results.copy())

        if args.webhook_url is not None:
            send_webhook(args.webhook_url, results)

        exported_results = deepcopy(results)

    return exported_results
