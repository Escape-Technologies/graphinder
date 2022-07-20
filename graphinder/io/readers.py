"""I/O readers."""

from io import TextIOWrapper

from graphinder.pool.domain import Domain
from graphinder.utils.filters import transform_url_in_domain
from graphinder.utils.logger import get_logger


def read_domains(
    file: TextIOWrapper | None,
    domain: str | None,
    precision_mode: bool = False,
) -> list[Domain]:
    """Read domains from file."""

    if domain is not None:
        if (clean := transform_url_in_domain(domain)) is not None:
            return [Domain(clean, precision_mode)]
        return []

    if file is None:
        get_logger().warning('no input file specified, skipping reading domains..')
        return []

    urls: list[str] = list(set(file.read().splitlines()))
    domains: list[Domain] = []
    for url in urls:
        if (clean := transform_url_in_domain(url)) is not None:
            domains.append(Domain(clean, precision_mode))

    get_logger().info(f'found { len(domains) } domains.')

    return domains
