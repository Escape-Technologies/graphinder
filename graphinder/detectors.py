"""All functions for detection."""

import requests

PAYLOAD = {'query': 'query{__typename}'}


def is_gql_endpoint(url: str) -> bool:
    """check if the supplies url is a graphql endpoint."""

    try:
        response = requests.post(url, json=PAYLOAD)
        _ = response.json()['data']['__typename']
        return True
    except Exception:
        return False
