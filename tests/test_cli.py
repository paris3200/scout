"""Test cases for the cli module."""
import click.testing
import pytest
from click.testing import CliRunner
from testfixtures import LogCapture

from scout import cli


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking the command-line interface."""
    return click.testing.CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(cli.main)
    assert result.exit_code == 0


def test_main_configures_logger(runner: CliRunner) -> None:
    """It outputs to log."""
    with LogCapture() as log:
        runner.invoke(cli.main)
    log.check(("root", "INFO", "Initializing run..."))
