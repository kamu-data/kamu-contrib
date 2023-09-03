DATE:=$(shell date +%F)
S3_CONTRIB_BASE_URL="https://s3.us-west-2.amazonaws.com/datasets.kamu.dev/odf/v1/contrib/"
S3_BACKUP_BASE_URL="https://s3.us-west-2.amazonaws.com/datasets.kamu.dev/odf/v1/contrib/"

.PHONY: strip-notebooks
strip-notebooks:
	find . -name '.ipynb_checkpoints' -type d -prune -exec rm -rf {} \;
	find . -name '*.ipynb' -type f -exec nbstripout {} \;

backup:
	aws s3 cp --recursive "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.mint-burn" "$(S3_BACKUP_BASE_URL)net.rocketpool.reth.mint-burn.$(DATE)"
	aws s3 cp --recursive "$(S3_CONTRIB_BASE_URL)com.cryptocompare.ohlcv.eth-usd" "$(S3_BACKUP_BASE_URL)com.cryptocompare.ohlcv.eth-usd.$(DATE)"
	aws s3 cp --recursive "$(S3_CONTRIB_BASE_URL)co.alphavantage.tickers.daily.spy" "$(S3_BACKUP_BASE_URL)co.alphavantage.tickers.daily.spy.$(DATE)"

purge:
	aws s3 rm --recursive "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.mint-burn"
	aws s3 rm --recursive "$(S3_CONTRIB_BASE_URL)com.cryptocompare.ohlcv.eth-usd"
	aws s3 rm --recursive "$(S3_CONTRIB_BASE_URL)co.alphavantage.tickers.daily.spy"

push:
	kamu push net.rocketpool.reth.mint-burn --to "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.mint-burn" --no-alias
	kamu push com.cryptocompare.ohlcv.eth-usd --to "$(S3_CONTRIB_BASE_URL)com.cryptocompare.ohlcv.eth-usd" --no-alias
	kamu push co.alphavantage.tickers.daily.spy --to "$(S3_CONTRIB_BASE_URL)co.alphavantage.tickers.daily.spy" --no-alias
