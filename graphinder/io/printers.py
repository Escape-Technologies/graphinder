"""I/O for prints."""

from graphinder.entities.io import Results


def display_results(results: Results) -> None:
    """Prints the results."""

    for domain in results:
        print(f'{domain} - {len(results[domain])}')
        for result in sorted(results[domain]):
            print(f'\t{result}')
