"""All functions for detection."""

import requests

PAYLOAD = {'query': 'query{__typename}'}


def is_gql_endpoint(url: str) -> bool:
    """check if the supplies url is a graphql endpoint."""

    print(url)

    try:  # Check if the endpoint is similar to graphQL

        response_rest = requests.post(url)
        _ = response_rest.json()['data']['__typename']
        return False

    except Exception:

        try:
            response_gql = requests.post(url, json=PAYLOAD)
            if response_gql.json().get('data', {}).get('__typename') is not None:
                return True
            if response_gql.json().get('errors', [{}])[0].get('message') is not None:
                return True

            return False

        except Exception:

            return False
