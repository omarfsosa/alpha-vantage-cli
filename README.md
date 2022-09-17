# Command line interface for Alpha Vantage APIs

Work in progress.


##  Get a Free Alpha Vantage Key

Visit http://www.alphavantage.co/support/#api-key


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
  crypto  Manages the Cryptocurrences APIs (Not yet implemented)
  data    Manages the Fundamental Data APIs (Not yet implemented)
  econ    Manages the Economic Indicators APIs (Not yet implemented)
  forex   Manages the Forex APIs (Not yet implemented)
  intel   Manages the Alpha Intelligence APIs (Not yet implemented)
  stock   Manages the Core Stocks APIs
  tech    Manages the Technical Indicators APIs (Not yet implemented)
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