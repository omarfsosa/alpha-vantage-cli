import json
import pathlib

import click

from . import factory


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


# --- Core Stocks APIs
@cli.group()
def stock():
    """
    Manages the Core Stocks APIs
    """


stock_intraday = stock.command(
    "intraday",
    help="""
    SYMBOL is the name of the equity of your choice. For example, IBM, AAPL"

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
        option_names="symbol interval adjusted outputsize datatype",
        option_values=dict(
            function="TIME_SERIES_INTRADAY",
        ),
        api_key_func=_get_api_key,
    )
)

stock_quote = stock.command(
    "quote",
    help="""
    Quote information for SYMBOL (IBM, AAPL, etc.).

    A lightweight alternative to the time series APIs, this service returns
    the price and volume information for a token of your choice.
    """,
)(
    factory.command_factory(
        option_names="symbol datatype",
        option_values=dict(
            function="GLOBAL_QUOTE",
        ),
        api_key_func=_get_api_key,
    )
)

stock_daily = stock.command(
    "daily",
    help="""
    Daily, as-traded time series data for SYMBOL

    This API returns raw (as-traded) daily time series (date, daily open,
    daily high, daily low, daily close, daily volume) of the global equity
    specified, covering 20+ years of historical data. If you are also
    interested in split/dividend-adjusted historical data, please use the
    daily-adjusted command, which covers adjusted close values and historical
    split and dividend events.
    """,
)(
    factory.command_factory(
        option_names="symbol outputsize datatype",
        option_values=dict(
            function="TIME_SERIES_DAILY",
        ),
        api_key_func=_get_api_key,
    )
)

stock_daily_adjusted = stock.command(
    "daily-adjusted",
    help="""
    Daily adjusted, as-traded time series data for SYMBOL.

    This API returns raw (as-traded) daily open/high/low/close/volume values,
    daily adjusted close values, and historical split/dividend events of the
    global equity specified, covering 20+ years of historical data.
    """,
)(
    factory.command_factory(
        option_names="symbol outputsize datatype",
        option_values=dict(
            function="TIME_SERIES_DAILY_ADJUSTED",
        ),
        api_key_func=_get_api_key,
    )
)

stock_weekly = stock.command(
    "weekly",
    help="""
    Weekly time series data for SYMBOL.

    This API returns weekly time series (last trading day of each week,
    weekly open, weekly high, weekly low, weekly close, weekly volume)
    of the global equity specified, covering 20+ years of historical data.
    """,
)(
    factory.command_factory(
        option_names="symbol datatype",
        option_values=dict(
            function="TIME_SERIES_WEEKLY",
        ),
        api_key_func=_get_api_key,
    )
)

stock_weekly_adjusted = stock.command(
    "weekly-adjusted",
    help="""
    Weekly adjusted time series data for SYMBOL.

    This API returns weekly adjusted time series (last trading day of each
    week, weekly open, weekly high, weekly low, weekly close, weekly adjusted
    close, weekly volume, weekly dividend) of the global equity specified,
    covering 20+ years of historical data.
    """,
)(
    factory.command_factory(
        option_names="symbol datatype",
        option_values=dict(
            function="TIME_SERIES_WEEKLY",
        ),
        api_key_func=_get_api_key,
    )
)

stock_monthly = stock.command(
    "monthly",
    help="""
    Monthly time series data for SYMBOL.

    This API returns monthly time series (last trading day of each month,
    monthly open, monthly high, monthly low, monthly close, monthly volume)
    of the global equity specified, covering 20+ years of historical data.
    """,
)(
    factory.command_factory(
        option_names="symbol datatype",
        option_values=dict(
            function="TIME_SERIES_MONTHLY",
        ),
        api_key_func=_get_api_key,
    )
)

stock_monthly_adjusted = stock.command(
    "monthly-adjusted",
    help="""
    Monthly adjusted time series data for SYMBOL.

    This API returns monthly adjusted time series (last trading day of each
    month, monthly open, monthly high, monthly low, monthly close, monthly
    adjusted close, monthly volume, monthly dividend) of the equity specified,
    covering 20+ years of historical data.
    """,
)(
    factory.command_factory(
        option_names="symbol datatype",
        option_values=dict(
            function="TIME_SERIES_MONTHLY",
        ),
        api_key_func=_get_api_key,
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


# --- Forex
@cli.group()
def forex():
    """
    Manages the Forex APIs (Not yet implemented)
    """


forex_intraday = forex.command(
    "intraday",
    help="""
    This API returns intraday time series (timestamp, open, high, low, close)
    of the FX currency pair FROM_SYMBOL-TO_SYMBOL specified, updated realtime.
    """,
)(
    factory.command_factory(
        option_names="from_symbol to_symbol interval outputsize datatype",
        option_values=dict(
            function="FX_INTRADAY",
        ),
        api_key_func=_get_api_key,
    )
)


forex_daily = forex.command(
    "daily",
    help="""
    This API returns the daily time series (timestamp, open, high, low, close)
    of the FX currency pair FROM_SYMBOL-TO_SYMBOL specified, updated realtime.
    """,
)(
    factory.command_factory(
        option_names="from_symbol to_symbol outputsize datatype",
        option_values=dict(
            function="FX_DAILY",
        ),
        api_key_func=_get_api_key,
    )
)


forex_weekly = forex.command(
    "weekly",
    help="""
    This API returns the weekly time series (timestamp, open, high, low, close)
    of the FX currency pair FROM_SYMBOL-TO_SYMBOL specified, updated realtime.
    The latest data point is the price information for the week (or partial
    week) containing the current trading day, updated realtime.
    """,
)(
    factory.command_factory(
        option_names="from_symbol to_symbol datatype",
        option_values=dict(
            function="FX_WEEKLY",
        ),
        api_key_func=_get_api_key,
    )
)


forex_monthly = forex.command(
    "monthly",
    help="""
    This API returns the monthly time series (timestamp, open, high, low,
    close) of the FX currency pair FROM_SYMBOL-TO_SYMBOL specified, updated
    realtime. The latest data point is the price information for the month (or
    partial month) containing the current trading day, updated realtime.
    """,
)(
    factory.command_factory(
        option_names="from_symbol to_symbol datatype",
        option_values=dict(
            function="FX_MONTHLY",
        ),
        api_key_func=_get_api_key,
    )
)


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
