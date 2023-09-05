DATE:=$(shell date +%F)
S3_CONTRIB_BASE_URL="s3://datasets.kamu.dev/odf/v1/contrib/"
S3_BACKUP_BASE_URL="s3://datasets.kamu.dev/odf/backup/"

.PHONY: strip-notebooks
strip-notebooks:
	find . -name '.ipynb_checkpoints' -type d -prune -exec rm -rf {} \;
	find . -name '*.ipynb' -type f -exec nbstripout {} \;


.PHONY: backup
backup:
	aws s3 cp --recursive "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.mint-burn" "$(S3_BACKUP_BASE_URL)net.rocketpool.reth.mint-burn.$(DATE)"
	aws s3 cp --recursive "$(S3_CONTRIB_BASE_URL)com.cryptocompare.ohlcv.eth-usd" "$(S3_BACKUP_BASE_URL)com.cryptocompare.ohlcv.eth-usd.$(DATE)"
	aws s3 cp --recursive "$(S3_CONTRIB_BASE_URL)co.alphavantage.tickers.daily.spy" "$(S3_BACKUP_BASE_URL)co.alphavantage.tickers.daily.spy.$(DATE)"


.PHONY: purge
purge:
	aws s3 rm --recursive "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.mint-burn"
	aws s3 rm --recursive "$(S3_CONTRIB_BASE_URL)com.cryptocompare.ohlcv.eth-usd"
	aws s3 rm --recursive "$(S3_CONTRIB_BASE_URL)co.alphavantage.tickers.daily.spy"


.PHONY: pull
pull:
	kamu pull "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.mint-burn"
	kamu pull "$(S3_CONTRIB_BASE_URL)com.cryptocompare.ohlcv.eth-usd"
	kamu pull "$(S3_CONTRIB_BASE_URL)co.alphavantage.tickers.daily.spy"


.PHONY: push
push:
	kamu push net.rocketpool.reth.mint-burn --to "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.mint-burn" --no-alias
	kamu push com.cryptocompare.ohlcv.eth-usd --to "$(S3_CONTRIB_BASE_URL)com.cryptocompare.ohlcv.eth-usd" --no-alias
	kamu push co.alphavantage.tickers.daily.spy --to "$(S3_CONTRIB_BASE_URL)co.alphavantage.tickers.daily.spy" --no-alias

.PHONY: push-ipfs
push-ipfs:
	.ci/push-to-ipfs.sh net.rocketpool.reth.mint-burn
	.ci/push-to-ipfs.sh com.cryptocompare.ohlcv.eth-usd
	.ci/push-to-ipfs.sh co.alphavantage.tickers.daily.spy
