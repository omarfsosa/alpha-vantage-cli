import pytest

from alpha_vantage_cli import factory


@pytest.fixture
def mock_requests_get(mocker):
    return mocker.patch("requests.get")


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
    result = factory.parse_options(["symbol", "interval", "outputsize"])
    assert result == tuple(["symbol", "interval", "outputsize"])

    with pytest.raises(ValueError):
        factory.parse_options("symbol badname")


def test_handle_values():
    values = {"symbol": "aapl", "interval": "30", "outputsize": "full"}
    handled = factory.handle_values(values)
    assert handled["symbol"].isupper()
    assert handled["interval"].endswith("min")
    assert values.keys() == handled.keys()

    values = {"outputsize": "full"}
    assert factory.handle_values(values) == values


def test_command_factory(requests_mock):
    option_names = "symbol interval datatype"
    option_values = {
        "function": "FUNCTION_NAME",
    }
    command = factory.command_factory(
        option_names,
        option_values,
        api_key_func=lambda: "testkey",
    )
    assert callable(command)

    # -- Mock the api responses:
    url = (
        "https://www.alphavantage.co/query?"
        "function=FUNCTION_NAME&apikey=testkey&symbol=IBM&interval=60min"
    )
    requests_mock.get(url, json={"example": "mocked-response"})
    requests_mock.get(url + "&datatype=csv", text="mocked-response")
    result = command(symbol="ibm", interval="60", datatype="json")
    assert result == {"example": "mocked-response"}
    result = command(symbol="ibm", interval="60", datatype="csv")
    assert result == "mocked-response"
