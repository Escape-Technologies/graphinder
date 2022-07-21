"""Provide datas to graphinder."""


def gql_endpoints_characterizer() -> list[str]:
    """return list of most common GQL endpoints."""

    characterizers: list[str] = [
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

    versioned_characterizers: list[str] = []
    versions = ['v1', 'v2']
    for version in versions:
        for char in characterizers:
            if any(v in char for v in versions):
                continue
            versioned_characterizers.append(f'{version}/{char}')

    return characterizers + versioned_characterizers
