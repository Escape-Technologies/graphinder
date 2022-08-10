"""I/O readers."""

from io import TextIOWrapper
from typing import List, Optional

from graphinder.pool.domain import Domain
from graphinder.utils.filters import transform_url_in_domain
from graphinder.utils.logger import get_logger


def read_domains(
    file: Optional[TextIOWrapper],
    domain: Optional[str],
    precision_mode: bool = False,
) -> List[Domain]:
    """Read domains from file."""

    if domain is not None:
        clean = transform_url_in_domain(domain)
        if clean is not None:
            return [Domain(clean, precision_mode)]
        return []

    if file is None:
        get_logger().warning('no input file specified, skipping reading domains..')
        return []

    urls: List[str] = list(set(file.read().splitlines()))
    domains: List[Domain] = []
    for url in urls:
        clean = transform_url_in_domain(url)
        if clean is not None:
            domains.append(Domain(clean, precision_mode))

    get_logger().info(f'found { len(domains) } domains.')

    return domains
