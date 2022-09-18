# Command line interface for Alpha Vantage APIs (WIP)

Command line interface to get stock data from the Alpha Vantage API

Alpha Vantage offers an API for financial data and other popular finance indicators. 
This library provides a series of commands that you can use to query the API from your terminal in an easy way.

###  Getting started

Get an alpha vantage free api key. Visit http://www.alphavantage.co/support/#api-key

Install ``alpha-vantage-cli``:
```bash
pip install alpha-vantage-cli
```

Set your api key:
```
av set-key
```

Try it out:
```bash
av stock quote ibm
```


## Usage examples

```bash
av --help
```

Output:

```
Usage: av [OPTIONS] COMMAND [ARGS]...

  Unofficial Alpha Vantage command line interaface.

  Get stocks data from the command line.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  crypto   Manages the Cryptocurrences APIs (Not yet implemented)
  data     Manages the Fundamental Data APIs (Not yet implemented)
  econ     Manages the Economic Indicators APIs (Not yet implemented)
  forex    Manages the Forex APIs (Not yet implemented)
  intel    Manages the Alpha Intelligence APIs (Not yet implemented)
  set-key  Set your API key so that you can send requests to Alpha...
  stock    Manages the Core Stocks APIs
  tech     Manages the Technical Indicators APIs (Not yet implemented)
```


### Get quote for stock

```bash
av stock quote aapl
```

Sample output:

```
{'Global Quote': {'01. symbol': 'AAPL', '02. open': '151.2100', '03. high': '151.3500', '04. low': '148.3700', '05. price': '150.7000', '06. volume': '162278841', '07. latest trading day': '2022-09-16', '08. previous close': '152.3700', '09. change': '-1.6700', '10. change percent': '-1.0960%'}}
```

### Download monthly data as CSV

```bash
av stock monthly ibm --datatype=csv > ibm.csv
```