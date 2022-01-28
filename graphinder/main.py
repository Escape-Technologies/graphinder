"""Main flow of the project."""
import sys

import click

from graphinder.graphinder import finder


def print_help() -> None:
    """Display help message."""
    ctx = click.get_current_context()
    click.echo(ctx.get_help())


@click.group(invoke_without_command=True)
def main() -> None:
    """Starting point."""

    if not sys.argv[1:]:
        print_help()


main.add_command(finder)
