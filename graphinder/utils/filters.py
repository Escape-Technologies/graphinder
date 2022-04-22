"""All filters functions."""

from graphinder.entities.pool import Url
from graphinder.io.providers import gql_endpoints_characterizer


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

    # Reconstruct the list of endpoints using the smaller one.
    filtered_urls: set[Url] = set()
    for _urls in unpacked_urls.values():
        filtered_urls.add(min(_urls, key=len))

    return filtered_urls
