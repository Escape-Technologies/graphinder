"""Discord webhook utils."""

import random
from typing import Any

import requests

from graphinder.entities.io import Results


def format_webhook(results: Results) -> dict:
    """Format embeds for webhook."""

    base: dict[str, Any] = {
        'username': 'Graphinder',
        'embeds': [],
    }

    for domain, urls in results.items():
        base['embeds'].append({
            'title': domain,
            'description': '\n'.join(urls),
            'color': random.randint(0, 16777215),
        })

    return base


def send_webhook(
    webhook_url: str,
    results: Results,
) -> bool:
    """Send discord webhook."""

    body = format_webhook(results)

    r = requests.post(url=webhook_url, json=body)

    return r.status_code == 204
