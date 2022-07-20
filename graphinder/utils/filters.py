"""All filters functions."""

import re

from graphinder.entities.pool import Url
from graphinder.io.providers import gql_endpoints_characterizer
from graphinder.utils.logger import get_logger


def filter_common(urls: set[str]) -> set[str]:
    """Remove commonly found urls in javascript files of a webpage such as w3.org."""

    common_strings = [
        'w3.org',
        'localhost',
        'schema.org',
        'sentry.io',
        'git.io',
        'github.com',
        'nuxtjs.org',
        'momentjs.com',
        'fb.me',
        'reactjs.org',
        'slack',
        'jquery',
        'google',
        'twitter',
        'elastic.co',
        'formatjs.io'
        'icann.org'  #TODO: find more of those
    ]

    urls_filtered = urls.copy()

    for url in urls:
        if '://a' in url and url.endswith('a'):
            urls_filtered.remove(url)
        elif '://x' in url and url.endswith('x'):
            urls_filtered.remove(url)
        else:
            for common_string in common_strings:
                if common_string in url:
                    urls_filtered.remove(url)

    return urls_filtered


def filter_urls(urls: set[Url]) -> set[Url]:
    """Remove urls that are not valid."""

    # We will re-populate the list of endpoints, sorted in len order to unpack them.
    _endpoints: list[str] = gql_endpoints_characterizer()
    _endpoints.sort(key=len, reverse=True)

    # Let's unpack the list of endpoints.
    unpacked_urls: dict[str, list[Url]] = {}
    for url in urls:
        for endpoint in _endpoints:
            if url.endswith(endpoint):

                unpacked_url = url.removesuffix(endpoint)
                if unpacked_url not in unpacked_urls:
                    unpacked_urls[unpacked_url] = []

                unpacked_urls[unpacked_url].append(url)

                break

    # Reconstruct the list of endpoints.
    # Attempt to find a full /graphql path.
    # Otherwise, use the smaller one.
    filtered_urls: set[Url] = set()
    for base_url, _urls in unpacked_urls.items():

        default_match: bool = False
        for _url in _urls:
            if _url[len(base_url):] == 'graphql':
                filtered_urls.add(_url)
                default_match = True

                break

        if not default_match:
            filtered_urls.add(min(_urls, key=len))

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


def transform_url_in_domain(url: str) -> str | None:
    """Transform a given url in domain.

    http(s)://(www.)
    """

    if 'https://' in url or 'http://' in url:  # here the url can even ben contained in a string it will still work (e.g. csv)
        if (search := re.search(r'(?:https?://(?:www.)?(?P<url>[^\s/]+)/?)', url)) is not None:
            return search.group('url')

        get_logger().error(f'{ url } does not contain any valid domain')
        return None

    # here the url is already a domain name
    return url.replace('www.', '').split('/')[0]
