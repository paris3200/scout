import click.testing

from scout import cli


def test_main_succeeds() -> None:
    """It exits with a status code of zero."""
    runner = click.testing.CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0


