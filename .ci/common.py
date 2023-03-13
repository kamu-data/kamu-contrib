import subprocess


EXTERNAL_DATASETS = {
  "com.cryptocompare.ohlcv.eth-usd",
  "co.alphavantage.tickers.daily.spy",
  "net.rocketpool.reth.mint-burn",
}

def is_external(id):
    return id in EXTERNAL_DATASETS
