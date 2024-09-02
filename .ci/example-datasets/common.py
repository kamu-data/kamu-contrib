import subprocess

S3_BASE_URL = "s3://datasets.kamu.dev/odf/v2/"
S3_CONTRIB_DATASETS_URL = f"{S3_BASE_URL}contrib/"
S3_EXAMPLE_DATASETS_URL = f"{S3_BASE_URL}example/"

EXTERNAL_DATASETS = {
  "com.cryptocompare.ohlcv.eth-usd": f"{S3_CONTRIB_DATASETS_URL}com.cryptocompare.ohlcv.eth-usd/",
  "co.alphavantage.tickers.daily.spy": f"{S3_CONTRIB_DATASETS_URL}co.alphavantage.tickers.daily.spy/",
  "net.rocketpool.reth.tokens-minted": f"{S3_CONTRIB_DATASETS_URL}net.rocketpool.reth.tokens-minted/",
  "net.rocketpool.reth.tokens-burned": f"{S3_CONTRIB_DATASETS_URL}net.rocketpool.reth.tokens-burned/",
  
  "com.github.kamu-data.clones": f"{S3_CONTRIB_DATASETS_URL}com.github.kamu-data.clones/",
  "com.github.kamu-data.stargazers": f"{S3_CONTRIB_DATASETS_URL}com.github.kamu-data.stargazers/",
  "com.github.kamu-data.views": f"{S3_CONTRIB_DATASETS_URL}com.github.kamu-data.views/",
  
  "com.youtube.channel.kamu-data.stats": f"{S3_CONTRIB_DATASETS_URL}com.youtube.channel.kamu-data.stats/",
  "com.youtube.channel.kamu-data.videos.stats": f"{S3_CONTRIB_DATASETS_URL}com.youtube.channel.kamu-data.videos.stats/",
  "com.youtube.playlist.featuring-kamu-data.videos.stats": f"{S3_CONTRIB_DATASETS_URL}com.youtube.playlist.featuring-kamu-data.videos.stats/",
}

def is_external(name):
    return name in EXTERNAL_DATASETS
