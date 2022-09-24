import json
import pathlib

import click
import toml

from alpha_vantage_cli import factory


def _get_path_credentials():
    return pathlib.Path.home() / ".alpha-vantage" / "credentials.json"


def _get_api_key():
    filepath = _get_path_credentials()
    with open(filepath) as f:
        credentials = json.load(f)

    return credentials["key"]


@click.group()
@click.version_option()
def cli():
    """
    Unofficial Alpha Vantage command line interaface.

    Get stocks data from the command line.
    """


@cli.command(
    name="set-key",
    help="""
    Set your API key so that you can send requests to Alpha Vantage's API. To
    request an API key visit https://www.alphavantage.co/support/#api-key
    """,
)
@click.option("--key", prompt=True, hide_input=True)
def set_key(key):
    path_save = _get_path_credentials()
    click.confirm(
        text=(
            f"Credentials will be stored at {path_save!s}.\n"
            "Do you wish to continue?"
        ),
        abort=True,
    )

    path_save.parent.mkdir(parents=True, exist_ok=True)
    credentials = {"key": key}
    with open(path_save, "w") as f:
        json.dump(credentials, f)


path_groups = pathlib.Path(__file__).parent / "groups"
for filepath in path_groups.iterdir():
    config = toml.load(filepath)
    group_name = config.pop("name")
    group_help = config.pop("help")
    group = cli.group(name=group_name, help=group_help)(lambda: None)
    for name, params in config.items():
        help_ = params["help"]
        group.command(name=name, help=help_)(
            factory.command_factory(
                option_names=params["options"],
                option_values=dict(
                    function=params["function"],
                ),
                api_key_func=_get_api_key,
            )
        )

# # --- Intelligence APIs
# @cli.group()
# def intel():
#     """
#     Manages the Alpha Intelligence APIs (Not yet implemented)
#     """


# @cli.group()
# def data():
#     """
#     Manages the Fundamental Data APIs (Not yet implemented)
#     """

# @cli.group()
# def crypto():
#     """
#     Manages the Cryptocurrences APIs (Not yet implemented)
#     """


# @cli.group()
# def econ():
#     """
#     Manages the Economic Indicators APIs (Not yet implemented)
#     """


# @cli.group()
# def tech():
#     """
#     Manages the Technical Indicators APIs (Not yet implemented)
#     """
