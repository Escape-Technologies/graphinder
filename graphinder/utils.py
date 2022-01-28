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
