from typing import Any, Iterable

import click
import requests

from alpha_vantage_cli import options

_base_url = "https://www.alphavantage.co/query?"
OptionNames = str | Iterable[str]
OptionValues = dict[str, Any]


def _fixes(**kwargs) -> str:
    return "&".join(f"{k}={v}" for k, v in kwargs.items())


def _allows(*args) -> str:
    return "&" + "&".join(f"{k!s}={{{k}}}" for k in args)


def make_query_string(*args, **kwargs) -> str:
    return _base_url + _fixes(**kwargs) + _allows(*args)


def parse_options(names: OptionNames) -> tuple[str]:
    if isinstance(names, str):
        names = names.replace(",", " ").split()

    if not all(hasattr(options, name) for name in names):
        raise ValueError("Names must all be valid options")

    return tuple(names)


def handle_values(d: dict[str, str]) -> dict[str, str]:
    if "symbol" in d:
        d["symbol"] = d["symbol"].upper()

    if "interval" in d:
        d["interval"] = d["interval"] + "min"

    return d


def command_factory(
    option_names: OptionNames,
    option_values: OptionValues,
    api_key_func: callable,
) -> callable:
    names = parse_options(option_names)
    query_fmt = make_query_string("apikey", *names, **option_values)

    def command(**kwargs):
        d = handle_values(kwargs)
        d["apikey"] = api_key_func()
        query = query_fmt.format(**d)
        response = requests.get(query)
        if d.get("datatype") == "json":
            result = response.json()
        elif d.get("datatype") == "csv":
            result = response.text
        else:
            result = response

        click.echo(result)

    for name in reversed(names):
        decorator = getattr(options, name)
        command = decorator(command)

    return command
