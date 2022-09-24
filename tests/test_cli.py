import pathlib
import time

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


@pytest.fixture
def mock_cli_get_api_key(mocker):
    mock = mocker.patch("alpha_vantage_cli.cli._get_api_key")
    mock.return_value = "demo"
    return mock


def test_cli_succeed(runner, mock_cli_get_api_key):
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0


@pytest.mark.parametrize("group", groups)
def test_group_succeed(runner, group, mock_cli_get_api_key):
    command = getattr(cli, group)
    result = runner.invoke(command)
    assert result.exit_code == 0


# --- end-to-end tests (these are skipped by nox by default)
args_file = pathlib.Path(__file__).parent / "args.txt"
with open(args_file, "r") as f:
    commands = f.read().splitlines()
    commands = [c for c in commands if c.startswith("forex")]


@pytest.mark.e2e
@pytest.mark.parametrize("args", commands)
def test_command(runner, args):
    # assert True
    result = runner.invoke(cli.cli, args=args)
    assert result.exit_code == 0
    # Sleep 15 seconds to avoid clogging the API
    time.sleep(15)
