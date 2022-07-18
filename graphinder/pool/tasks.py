"""Define tasks for the pool."""

import argparse
import asyncio

import aiohttp

from graphinder.entities.tasks import Task, TasksList, TaskTags
from graphinder.io.providers import gql_endpoints_characterizer
from graphinder.pool.domain import Domain, Url


def generate_scripts_tasks(domain: Domain) -> TasksList:
    """Generate scripts tasks."""

    tasks: TasksList = []

    for subdomain in domain.subdomains:
        if subdomain:
            tasks.append(Task(domain.url, TaskTags.FETCH_PAGE_SCRIPTS, f'http://{subdomain}/'))

    domain.logger.debug(f'{len(tasks)} scripts tasks generated.')
    return tasks


def generate_bruteforce_tasks(domain: Domain) -> TasksList:
    """Generate bruteforce tasks."""

    tasks: TasksList = []

    for subdomain in domain.subdomains:
        if subdomain:
            for directory in gql_endpoints_characterizer():
                url: str = f'http://{subdomain.removesuffix("/graphql").rstrip("/")}' + '/' + directory
                tasks.append(Task(domain.url, TaskTags.FETCH_ENDPOINT, url))

    domain.logger.debug(f'{len(tasks)} bruteforce tasks generated.')
    return tasks


def generate_tasks(
    domain: Domain,
    args: argparse.Namespace,
) -> TasksList:
    """Generate tasks depending on settings."""

    tasks: TasksList = []

    if args.script_mode:
        tasks += generate_scripts_tasks(domain)

    if args.bruteforce_mode:
        tasks += generate_bruteforce_tasks(domain)

    domain.logger.info(f'{len(tasks)} tasks generated.')
    return tasks


def init_domain_tasks(
    domain: Domain,
    args: argparse.Namespace,
) -> TasksList:
    """Init domain tasks."""

    domain.fetch_subdomains(args.reduce_mode)
    return generate_tasks(domain, args)


async def add_tasks(domain: Domain, urls: set[Url], tag: TaskTags) -> None:
    """Add tasks."""

    for url in urls:
        asyncio.create_task(process_task(Task(domain.url, tag, url), domain))


async def process_task(
    task: Task,
    domain: Domain,
) -> None:
    """Process task."""

    # precision_mode: Lock the task semaphore for the given domain.
    if domain.semaphore:
        await domain.semaphore.acquire()

    # process task using the correct method.
    if task.tag == TaskTags.FETCH_SCRIPT:
        _urls = await domain.fetch_script(task.url)
        if _urls:
            await add_tasks(domain, _urls, TaskTags.FETCH_ENDPOINT)
    elif task.tag == TaskTags.FETCH_PAGE_SCRIPTS:
        _urls = await domain.fetch_page_scripts(task.url)
        if _urls:
            await add_tasks(domain, _urls, TaskTags.FETCH_SCRIPT)
    elif task.tag == TaskTags.FETCH_ENDPOINT:
        await domain.fetch_endpoint(task.url)
    else:
        raise NotImplementedError()

    # precision_mode: Release semaphore for the given domain.
    if domain.semaphore:
        domain.semaphore.release()


async def consume_tasks(
    tasks: TasksList,
    domain: Domain,
) -> set[Url]:
    """Consume tasks."""

    connector = aiohttp.TCPConnector(limit=100, ttl_dns_cache=600)
    domain.session = aiohttp.ClientSession(connector=connector)

    await asyncio.gather(*[process_task(task, domain) for task in tasks])

    await domain.session.close()

    return domain.results
