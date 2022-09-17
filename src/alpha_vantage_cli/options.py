import click


symbol = click.option(
    "--symbol",
    "-s",
    type=str,
    required=True,
    help="The name of the equity of your choice. For example, IBM, APPL",
)

interval = click.option(
    "--interval",
    "-i",
    type=click.Choice(["1", "5", "15", "30", "60"]),
    required=False,
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
    "--outputsize", type=click.Choice(["compact", "full"]), default="compact"
)

datatype = click.option(
    "--datatype", type=click.Choice(["json", "csv"]), default="json"
)
