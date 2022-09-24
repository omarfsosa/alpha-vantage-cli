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
    return "&".join(f"{k!s}={{{k}}}" for k in args)


def make_query_string(*args, **kwargs) -> str:
    suffix = "&".join([_fixes(**kwargs), _allows(*args)])
    return _base_url + suffix


def parse_options(names: OptionNames) -> tuple[str]:
    if isinstance(names, str):
        names = names.replace(",", " ").split()

    return tuple(names)


def handle_values(d: dict[str, str]) -> dict[str, str]:
    if "symbol" in d:
        d["symbol"] = d["symbol"].upper()

    if "interval" in d:
        d["interval"] = d["interval"] + "min"

    return d


def build_query(query_fmt, api_key_func, **kwargs):
    kwargs = handle_values(kwargs)
    kwargs["apikey"] = api_key_func()
    query = query_fmt.format(**kwargs)
    return query


def command_factory(
    option_names: OptionNames,
    option_values: OptionValues,
    api_key_func: callable,
) -> callable:
    names = parse_options(option_names)
    arg_names = []
    for name in names:
        renamed = options.option_name_to_query_name.get(name, name)
        arg_names.append(renamed)

    query_fmt = make_query_string("apikey", *arg_names, **option_values)

    def command(**kwargs):
        query = build_query(query_fmt, api_key_func, **kwargs)
        datatype = kwargs.get("datatype")
        response = requests.get(query)
        # TODO: Raise if response is not 200

        if datatype is None or datatype.lower() == "json":
            result = response.json()
            click.echo(result)
            return result

        if datatype.lower() == "csv":
            result = response.text
            click.echo(result)
            return result

    for name in reversed(names):
        decorator = getattr(options, name)
        command = decorator(command)

    return command
