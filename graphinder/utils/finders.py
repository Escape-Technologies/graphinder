"""All finder utils used by extractors."""

import re


def find_script_full_urls(script_file: str) -> list[str]:
    """Extract full urls from script file."""

    return re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', script_file)


def find_script_window_base_urls(
    domain: str,
    script_file: str,
) -> list[str]:
    """Extract window.__BASE_URL__ urls from script file.

    window.__BASE_URL__ +"/graphql" window.__BASE_URL__+"/api/graphql" window.__BASE_URL__ + "/api/v1/graphql"
    """

    urls: list[str] = re.findall(r'window.__BASE_URL__ ?\+ ?\"\S{0,15}/graphql\"+', script_file)

    # Replace window.__BASE_URL__ with domain and strip ending `"`
    return [domain + url[url.find('"') + 1:-1] for url in urls]


def find_script_fetch_graphql(
    domain: str,
    script_file: str,
) -> list[str]:
    """Extract potential fetch/axios("/graphql") urls from script file.

    ("/graphql" ("/api/graphql" ("/api/v1/graphql"
    """

    urls: list[str] = re.findall(r'\(\"\S{0,15}/graphql\"+', script_file)

    # Remove starting `("` and ending `"`
    return [domain + url[2:-1] for url in urls]
