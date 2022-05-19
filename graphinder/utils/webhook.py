"""Discord webhook utils."""

from typing import Any

import requests

from graphinder.entities.io import Results


def format_webhook(results: Results) -> dict:
    """Format embeds for webhook."""

    base: dict[str, Any] = {
        'content': None,
        'username': 'Graphinder',
        'embeds': [],
    }

    for domain, urls in results.items():
        base['embeds'].append({
            'title': domain,
            'description': '\n'.join(urls),
            'color': '#ffffff',
        })

    return base


def send_webhook(webhook_url: str, results: Results) -> bool:
    """Send discord webhook."""

    body = format_webhook(results)

    r = requests.post(url=webhook_url, json=body)
    print(r.status_code)
    print(r.text)

    return r.status_code == 200
