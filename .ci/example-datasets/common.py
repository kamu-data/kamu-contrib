import subprocess

S3_BASE_URL = "s3://datasets.kamu.dev/odf/v2/"
S3_CONTRIB_DATASETS_URL = f"{S3_BASE_URL}contrib/"
S3_EXAMPLE_DATASETS_URL = f"{S3_BASE_URL}example/"

EXTERNAL_DATASETS = {
  "com.cryptocompare.ohlcv.eth-usd": f"{S3_CONTRIB_DATASETS_URL}com.cryptocompare.ohlcv.eth-usd/",
  "co.alphavantage.tickers.daily.spy": f"{S3_CONTRIB_DATASETS_URL}co.alphavantage.tickers.daily.spy/",
  "net.rocketpool.reth.mint-burn": f"{S3_CONTRIB_DATASETS_URL}net.rocketpool.reth.mint-burn/",
}

def is_external(name):
    return name in EXTERNAL_DATASETS
