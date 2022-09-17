import json

import click.testing
import pytest

from alpha_vantage_cli import cli


groups = (
    "stock",
    "intel",
    "data",
    "forex",
    "crypto",
    "econ",
    "tech",
)


@pytest.fixture
def runner():
    return click.testing.CliRunner()


@pytest.fixture
def mock_requests_get(mocker):
    return mocker.patch("requests.get")


def test_cli_succeed(runner):
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0


@pytest.mark.parametrize("group", groups)
def test_group_succeed(runner, group):
    command = getattr(cli, group)
    result = runner.invoke(command)
    assert result.exit_code == 0


# --- end-to-end tests (these are skipped by nox by default)
@pytest.mark.e2e
def test_av_stock_quote_in_production_env(runner):
    """
    This test sends an actual request to Alpha Vantage
    API and so it can fail for external reasons too.
    """
    result = runner.invoke(cli.stock_quote, args="ibm")
    assert result.exit_code == 0
    assert isinstance(json.loads(result.output), dict)
