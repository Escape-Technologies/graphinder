"""I/O readers."""

from io import TextIOWrapper

from graphinder.pool.domain import Domain
from graphinder.utils.logger import get_logger


def read_domains(file: TextIOWrapper | None, domain: str | None) -> list[Domain]:
    """Read domains from file."""

    if domain is not None:
        return [Domain(domain)]

    if file is None:
        get_logger('io').critical('no input file specified, skipping reading domains..')
        return []

    urls: list[str] = list(set(file.read().splitlines()))
    domains: list[Domain] = [Domain(url) for url in urls]

    get_logger('io').success(f'found { len(domains) } domains.')

    return domains
