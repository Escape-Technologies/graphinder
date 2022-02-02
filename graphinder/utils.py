"""utilities functions that are needed."""

from copy import deepcopy


def filter_common(urls: list[str]) -> list[str]:
    """remove commonly found urls in javascript files of a webpage such as w3.org."""
    filtered_urls: list[str] = deepcopy(urls)

    common_strings = [
        'w3.org',
        'localhost',
        'sentry.io',
        'git.io',
        'github.com',
        'nuxtjs.org',
        'momentjs.com',
        'google'  #TODO: find more of those
    ]

    for url in urls:
        for common_string in common_strings:
            if common_string in url:
                filtered_urls.remove(url)

    return filtered_urls


def remove_duplicate_domains(domains: list[str]) -> list[str]:
    """if domains has example.com and www.example.com this will remove www.example.com."""
    corrected_domains = []

    for domain in domains:
        if domain.startswith('www.'):
            if domain.lstrip('www.') in domains:
                continue
        corrected_domains.append(domain)

    return corrected_domains


def reduce_domains(domains: list[str]) -> list[str]:
    """reduces a list of subdomains to a list constaining only the domains most probable to contain GQL endpoint."""
    reduced = []
    for domain in domains:
        if 'app' in domain or 'api' in domain or 'dev' in domain or 'graphql' in domain:
            reduced.append(domain)
    return reduced


def format_dict(input_list: list) -> dict:
    """given list will output a dict with the list elements as keys and sets values to []"""

    list_dict: dict = {}

    for elem in input_list:
        list_dict[elem] = []

    return list_dict
