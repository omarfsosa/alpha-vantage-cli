import click

symbol = click.argument(
    "symbol",
    type=str,
    required=True,
)

interval = click.option(
    "--interval",
    "-i",
    type=click.Choice(["1", "5", "15", "30", "60"]),
    default="60",
    help=(
        "Time interval (in minutes) between two consecutive data points in"
        " the time series. The following values are supported: 1, 5, 15, 30"
        ", 60."
    ),
)

adjusted = click.option(
    "--adjusted/--no-adjusted",
    default=True,
    help="By default, the output time series is adjusted by historical split"
    "and dividend events. Set --no-adjusted to query raw (as-traded) intraday"
    "values.",
)

outputsize = click.option(
    "--outputsize",
    type=click.Choice(["compact", "full"]),
    default="compact",
    help="Compact by default. This returns only the latest 100 data points "
    "in the time series;  using --outputsize=full returns the full-length"
    " time series. The compact option is recommended if you would like to "
    "reduce the data size of each API call.",
)

datatype = click.option(
    "--datatype",
    type=click.Choice(["json", "csv"]),
    default="json",
    help="""
    By default, --datatype=json. Strings json and csv are accepted with the
    following specifications: --datatype=json returns the time series in JSON
    format; --datatype=csv returns the time series as a CSV (comma separated
    value) file.
    """,
)
