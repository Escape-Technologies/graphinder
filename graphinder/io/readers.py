"""I/O readers."""

from io import TextIOWrapper

from graphinder.pool.domain import Domain
from graphinder.utils.filters import transform_url_in_domain
from graphinder.utils.logger import get_logger


def read_domains(file: TextIOWrapper | None, domain: str | None, precision_mode: bool = False) -> list[Domain]:
    """Read domains from file."""

    if domain is not None:
        return [Domain(transform_url_in_domain(domain), precision_mode)]

    if file is None:
        get_logger('io').critical('no input file specified, skipping reading domains..')
        return []

    urls: list[str] = list(set(file.read().splitlines()))
    domains: list[Domain] = [Domain(transform_url_in_domain(url), precision_mode) for url in urls]

    get_logger('io').success(f'found { len(domains) } domains.')

    return domains
