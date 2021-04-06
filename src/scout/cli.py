"""Command Line Interface."""

import logging

import click

from . import __version__, config


@click.command()
@click.version_option(version=__version__)
def main() -> None:
    """Scout - the price tracker."""
    logging.basicConfig(
        filename=config.LOGFILE,
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logging.info("Initializing run...")
