"""Provide datas to graphinder."""

from typing import List


def gql_endpoints_characterizer() -> List[str]:
    """Return list of most common GQL endpoints.

    - Versioning has a huge cost on the performance of the scanner.
    - We try to minimize the cost by using the most common endpoints only.
    """

    characterizers: List[str] = [
        'graphql',
        'appsync',
        'altair',
        'explorer',
        'graphiql',
        'playground',
        'subscriptions',
        'graph',
        'graphiql.css',
        'graphiql/finland',
        'graphiql.js',
        'graphiql.min.css',
        'graphiql.min.js',
        'graphiql.php',
        'graphql/console',
        'graphql-explorer',
        'graphql.php',
        'graphql/schema.json',
        'graphql/schema.xml',
        'graphql/schema.yaml',
        'graphql/v1',
        'graphql/v2',
        'api/graphql',
    ]

    versioned_characterizers: List[str] = []
    versions = ['v1', 'v2']
    for version in versions:
        for char in characterizers[:8]:
            if any(v in char for v in versions):
                continue
            versioned_characterizers.append(f'{version}/{char}')

    return characterizers + versioned_characterizers
