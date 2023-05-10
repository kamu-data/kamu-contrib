import subprocess


EXTERNAL_DATASETS = {
  "com.cryptocompare.ohlcv.eth-usd": "s3://datasets.kamu.dev/com.cryptocompare.ohlcv.eth-usd/",
  "co.alphavantage.tickers.daily.spy": "s3://datasets.kamu.dev/co.alphavantage.tickers.daily.spy/",
  "net.rocketpool.reth.mint-burn": "s3://datasets.kamu.dev/net.rocketpool.reth.mint-burn/",
}

def is_external(id):
    return id in EXTERNAL_DATASETS
