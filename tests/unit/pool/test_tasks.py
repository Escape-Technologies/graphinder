# pylint: disable=redefined-outer-name

"""Test pool/tasks.py."""

import argparse
import asyncio

import aiohttp
import pytest

from graphinder.entities.tasks import Task, TasksList, TaskTags
from graphinder.io.providers import gql_endpoints_characterizer
from graphinder.main import argument_builder
from graphinder.pool.domain import Domain, Url
from graphinder.pool.tasks import add_tasks, generate_bruteforce_tasks, generate_scripts_tasks, generate_tasks, init_domain_tasks, process_task
from graphinder.utils.assets import fetch_assets


@pytest.fixture
def domain() -> Domain:
    """Domain fixture."""

    _domain: Domain = Domain(Url('example.com'))
    _domain.subdomains = ['api.example.com', 'test.example.com']

    return _domain


def test_generate_scripts_tasks(domain: Domain) -> None:
    """generate_scripts_tasks test."""

    tasks: TasksList = generate_scripts_tasks(domain)

    assert len(tasks) == 2, 'There should be 2 tasks.'


def test_generate_bruteforce_tasks(domain: Domain) -> None:
    """generate_bruteforce_tasks test."""

    tasks: TasksList = generate_bruteforce_tasks(domain)

    assert len(tasks) == 2 * len(gql_endpoints_characterizer()), 'There should be 2 * gql_endpoints_characterizer tasks.'


def test_generate_tasks(domain: Domain) -> None:
    """generate_tasks test."""

    args: argparse.Namespace = argument_builder([])

    tasks: TasksList = generate_tasks(domain, args)
    assert len(tasks) == 2 * len(gql_endpoints_characterizer()) + 2, 'There should be 2 * gql_endpoints_characterizer + 2 tasks.'

    args = argument_builder(['--no-script'])
    tasks = generate_tasks(domain, args)
    assert len(tasks) == 2 * len(gql_endpoints_characterizer()), 'There should be 2 * gql_endpoints_characterizer tasks.'

    args = argument_builder(['--no-bruteforce'])
    tasks = generate_tasks(domain, args)
    assert len(tasks) == 2, 'There should be 2 tasks.'

    args = argument_builder(['--no-script', '--no-bruteforce'])
    tasks = generate_tasks(domain, args)
    assert len(tasks) == 0, 'There should be 0 tasks.'


def test_init_domain_tasks(domain: Domain) -> None:
    """init_domain_tasks test."""

    fetch_assets()

    tasks: TasksList = init_domain_tasks(domain, argument_builder([]))

    assert len(tasks) == 100 * len(gql_endpoints_characterizer()) + 100, 'There should be 100 * gql_endpoints_characterizer + 100 tasks.'


@pytest.mark.asyncio
async def test_add_tasks() -> None:
    """add_tasks test."""

    async with aiohttp.ClientSession() as session:
        assert len(asyncio.all_tasks()) == 1, 'There should be 1 tasks.'

        await add_tasks(Domain(Url('example.com')), {Url('http://example.com/')}, TaskTags.FETCH_PAGE_SCRIPTS, session)

        assert len(asyncio.all_tasks()) == 2, 'There should be 2 tasks.'


@pytest.mark.asyncio
async def test_process_task() -> None:
    """process_task test."""

    async with aiohttp.ClientSession() as session:
        assert len(asyncio.all_tasks()) == 1, 'There should be 1 tasks.'

        try:
            await process_task(Task('example.com', 'unknown tag', 'example.com'), session, 'example.com')  # type: ignore
            assert False, 'Unknown tag should raise an error.'
        except NotImplementedError:
            pass


@pytest.mark.asyncio
async def test_consume_tasks() -> None:
    """consume_tasks test."""
