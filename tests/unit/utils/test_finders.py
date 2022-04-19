"""Test utils/finders.py."""

from graphinder.utils.finders import find_script_fetch_graphql, find_script_full_urls, find_script_window_base_urls


def test_find_script_full_urls() -> None:
    """find_script_full_urls test."""

    script_file: str = """
        https://example.com
        https://apps.example.com
        https://www.example.com
    """

    urls: list[str] = find_script_full_urls(script_file)

    assert urls == [
        'https://example.com',
        'https://apps.example.com',
        'https://www.example.com',
    ]


def test_find_script_window_base_urls() -> None:
    """find_script_window_base_urls test."""

    script_file: str = """
        {var e=new ze({uri:window.__BASE_URL__+"/graphql",credentials:"same-origin"}
        window.__BASE_URL__+"/api/graphql"
        window.__BASE_URL__ + "/api/v1/graphql"
    """

    urls: list[str] = find_script_window_base_urls('https://example.com', script_file)

    assert urls == [
        'https://example.com/graphql',
        'https://example.com/api/graphql',
        'https://example.com/api/v1/graphql',
    ]


def test_find_script_fetch_graphql() -> None:
    """find_script_fetch_graphql test."""

    script_file: str = """
        function s(e){return e.options.siteId?fetch("/graphql",{method:"POST",credentials:"same-origin",headers:{"Content-Type":"application/json"},body:JSON.stringify({query:"{ me { id ...
        fetch("/api/graphql")
        fetch("/api/v1/graphql")
    """

    urls: list[str] = find_script_fetch_graphql('https://example.com', script_file)

    assert urls == [
        'https://example.com/graphql',
        'https://example.com/api/graphql',
        'https://example.com/api/v1/graphql',
    ]
