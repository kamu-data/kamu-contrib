import subprocess

S3_BASE_URL = "s3://datasets.kamu.dev/odf/v1/"
S3_EXAMPLE_DATASETS_URL = f"{S3_BASE_URL}example/"

EXTERNAL_DATASETS = {
  "com.cryptocompare.ohlcv.eth-usd": f"{S3_BASE_URL}contrib/com.cryptocompare.ohlcv.eth-usd/",
  "co.alphavantage.tickers.daily.spy": f"{S3_BASE_URL}contrib/co.alphavantage.tickers.daily.spy/",
  "net.rocketpool.reth.mint-burn": f"{S3_BASE_URL}contrib/net.rocketpool.reth.mint-burn/",
}

def is_external(id):
    return id in EXTERNAL_DATASETS
