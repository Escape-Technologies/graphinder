"""Functions to manage pooling."""

import argparse
from typing import Dict, Set, Union, cast

from graphinder.entities.io import Results
from graphinder.entities.tasks import TasksList
from graphinder.io.printers import display_results
from graphinder.io.writers import write_results
from graphinder.pool.domain import Domain, Url
from graphinder.pool.tasks import consume_tasks, init_domain_tasks
from graphinder.utils.filters import filter_urls
from graphinder.utils.logger import get_logger
from graphinder.utils.webhook import send_webhook


async def domain_routine(
    domain: Domain,
    args: argparse.Namespace,
) -> Dict[str, Union[str, Set[Url]]]:
    """Start domain routine."""

    _tasks: TasksList = init_domain_tasks(domain, args)
    _urls: Set[Url] = await consume_tasks(_tasks, domain)

    return {'domain': domain.url, 'urls': filter_urls(_urls)}


async def main_routine(args: argparse.Namespace) -> Results:
    """Main pool routine."""

    logger = get_logger()
    logger.info('starting main routine..')

    domain: Domain = Domain(args.domain, args.precision_mode)
    logger.info(f'running scan on {domain.url}')

    output_file = args.output_file
    del args.output_file

    result = await domain_routine(domain, args)
    results: Results = cast(Results, {result['domain']: result['urls']})

    if not args.quiet_mode:
        display_results(results)

    if output_file is not None:
        write_results(output_file, results.copy())

    if args.webhook_url is not None:
        send_webhook(args.webhook_url, results)

    return results
