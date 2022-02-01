"""All functions for detection."""

import requests

PAYLOAD = {'query': 'query{__typename}'}


def is_gql_endpoint(url: str) -> bool:
    """check if the supplies url is a graphql endpoint."""

    try:  # Check if the endpoint is similar to graphQL

        response_rest = requests.post(url)
        _ = response_rest.json()['data']['__typename']
        return False

    except Exception:

        try:
            response_gql = requests.post(url, json=PAYLOAD)
            _ = response_gql.json()['data']['__typename']
            return True
        except Exception:
            return False
