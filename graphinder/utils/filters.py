"""All filters functions."""

from graphinder.entities.pool import Url
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

    urls_filtered = urls.copy()

    for url in urls:
        _slashs: int = url.count('/')

        if url not in urls_filtered:
            continue

        if _slashs < 3:
            get_logger('filter').error(f'Removing invalid url: {url}')
            continue

        subdomain: str = '/'.join(url.split('/')[:3]) + '/'
        for _url in urls:

            # Check if the url has been removed from filter already
            if url not in urls_filtered or _url == url:
                continue

            # Make sure we are on the same directory, not in /api or whatever
            if _url.count('/') != _slashs:
                continue

            # Always keep the shortest url
            if subdomain in _url and len(_url) > len(url):
                if 'v2' in url and not 'v2' in _url:
                    continue
                if 'v1' in url and not 'v1' in _url:
                    continue

                urls_filtered.remove(url)

    return urls_filtered
