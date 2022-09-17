import os

import click

from . import factory


KEY_ENV_NAME = "ALPHA_VANTAGE_KEY"


def _key():
    return os.environ[KEY_ENV_NAME]


@click.group()
@click.version_option()
def cli():
    """
    Unofficial Alpha Vantage command line interaface.

    Get stocks data from the command line.
    """


# --- Core Stocks APIs
@cli.group()
def stock():
    """
    Manages the Core Stocks APIs
    """


stock.command(
    "intraday",
    help="""
    This API returns intraday time series of the equity specified, covering
    extended trading hours where applicable (e.g., 4:00am to 8:00pm Eastern
    Time for the US market). The intraday data is derived from the
    Securities Information Processor (SIP) market-aggregated data. You can
    query both raw (as-traded) and split/dividend-adjusted intraday data from
    this endpoint.

    This API returns the most recent 1-2 months of intraday data and is best
    suited for short-term/medium-term charting and trading strategy
    development. If you are targeting a deeper intraday history, please use
    the Extended Intraday API.
    """,
)(
    factory.command_factory(
        "symbol interval adjusted outputsize datatype",
        function="TIME_SERIES_INTRADAY",
        apikey=_key(),
    )
)

stock.command(
    "quote",
    help="""
    A lightweight alternative to the time series APIs, this service returns
    the price and volume information for a token of your choice.
    """,
)(
    factory.command_factory(
        "symbol datatype",
        function="GLOBAL_QUOTE",
        apikey=_key(),
    )
)


stock.command(
    "daily",
    help="""
    This API returns raw (as-traded) daily time series (date, daily open,
    daily high, daily low, daily close, daily volume) of the global equity
    specified, covering 20+ years of historical data. If you are also
    interested in split/dividend-adjusted historical data, please use the
    Daily Adjusted API, which covers adjusted close values and historical
    split and dividend events.
    """,
)(
    factory.command_factory(
        "symbol outputsize datatype",
        function="TIME_SERIES_DAILY",
        apikey=_key(),
    )
)


stock.command(
    "weekly",
    help="""
    This API returns weekly time series (last trading day of each week,
    weekly open, weekly high, weekly low, weekly close, weekly volume)
    of the global equity specified, covering 20+ years of historical data.
    """,
)(
    factory.command_factory(
        "symbol datatype",
        function="TIME_SERIES_WEEKLY",
        apikey=_key(),
    )
)

stock.command(
    "monthly",
    help="""
    This API returns monthly time series (last trading day of each month,
    monthly open, monthly high, monthly low, monthly close, monthly volume)
    of the global equity specified, covering 20+ years of historical data.
    """,
)(
    factory.command_factory(
        "symbol datatype",
        function="TIME_SERIES_MONTHLY",
        apikey=_key(),
    )
)


# --- Intelligence APIs
@cli.group()
def intel():
    """
    Manages the Alpha Intelligence APIs (Not yet implemented)
    """


@cli.group()
def data():
    """
    Manages the Fundamental Data APIs (Not yet implemented)
    """


@cli.group()
def forex():
    """
    Manages the Forex APIs (Not yet implemented)
    """


@cli.group()
def crypto():
    """
    Manages the Cryptocurrences APIs (Not yet implemented)
    """


@cli.group()
def econ():
    """
    Manages the Economic Indicators APIs (Not yet implemented)
    """


@cli.group()
def tech():
    """
    Manages the Technical Indicators APIs (Not yet implemented)
    """
