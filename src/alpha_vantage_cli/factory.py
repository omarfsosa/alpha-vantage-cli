import click
import requests

from alpha_vantage_cli import options


_base_url = "https://www.alphavantage.co/query?"


def _fixes(**kwargs):
    return "&".join(f"{k}={v}" for k, v in kwargs.items())


def _allows(*args):
    return "&" + "&".join(f"{k!s}={{{k}}}" for k in args)


def make_query_string(*args, **kwargs):
    return _base_url + _fixes(**kwargs) + _allows(*args)


def parse_identifiers(names):
    if isinstance(names, str):
        names = names.replace(",", " ").split()

    return tuple(names)


def handle_inputs(dict_):
    if "symbol" in dict_:
        dict_["symbol"] = dict_["symbol"].upper()

    if "interval" in dict_:
        dict_["interval"] = dict_["interval"] + "min"

    return dict_


def command_factory(field_names, **fixed_fields):
    names = parse_identifiers(field_names)
    query_fmt = make_query_string(*names, **fixed_fields)

    def command(**kwargs):
        d = handle_inputs(kwargs)
        query = query_fmt.format(**d)
        response = requests.get(query)
        if d.get("datatype") == "json":
            result = response.json()
        elif d.get("datatype") == "csv":
            result = response.text
        else:
            raise ValueError("Missing datatype")

        click.echo(result)

    for name in reversed(names):
        decorator = getattr(options, name)
        cmd = decorator(command)

    return cmd
