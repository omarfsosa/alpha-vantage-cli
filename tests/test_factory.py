import pytest

from alpha_vantage_cli import factory


def test_make_query_string():
    query_fmt = factory.make_query_string(
        "param1",
        "param2",
        param3="fixed1",
        param4="fixed2",
    )

    assert query_fmt.startswith(factory._base_url)
    assert query_fmt.count("param1") == 2
    assert query_fmt.count("param2") == 2
    assert query_fmt.count("param3") == 1
    assert query_fmt.count("param4") == 1
    assert "param3=fixed1" in query_fmt
    assert "param4=fixed2" in query_fmt


def test_parse_options():
    result = factory.parse_options("symbol, interval outputsize")
    assert result == ("symbol", "interval", "outputsize")
    result = factory.parse_options("symbol")
    assert result == ("symbol",)

    with pytest.raises(ValueError):
        factory.parse_options("symbol badname")


def test_handle_values():
    values = {
        "symbol": "aapl",
        "interval": "30",
        "outputsize": "full"
    }
    handled = factory.handle_values(values)
    assert handled["symbol"].isupper()
    assert handled["interval"].endswith("min")
    assert values.keys() == handled.keys()


def test_command_factory():
    option_names = "symbol interval"
    option_values = {
        "function": "FUNCTION_NAME",
        "apikey": "testkey",
    }
    command = factory.command_factory(option_names, option_values)
    assert callable(command)
