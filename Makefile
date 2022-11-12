DATE:=$(shell date +%F)

.PHONY: strip-notebooks
strip-notebooks:
	find . -name '.ipynb_checkpoints' -type d -prune -exec rm -rf {} \;
	find . -name '*.ipynb' -type f -exec nbstripout {} \;

backup:
	aws s3 cp --recursive s3://datasets.kamu.dev/net.rocketpool.reth.mint-burn s3://datasets.kamu.dev/backups/net.rocketpool.reth.mint-burn.$(DATE)
	aws s3 cp --recursive s3://datasets.kamu.dev/com.cryptocompare.ohlcv.eth-usd s3://datasets.kamu.dev/backups/com.cryptocompare.ohlcv.eth-usd.$(DATE)
	aws s3 cp --recursive s3://datasets.kamu.dev/co.alphavantage.tickers.daily.spy s3://datasets.kamu.dev/backups/co.alphavantage.tickers.daily.spy.$(DATE)

purge:
	aws s3 rm --recursive s3://datasets.kamu.dev/net.rocketpool.reth.mint-burn
	aws s3 rm --recursive s3://datasets.kamu.dev/com.cryptocompare.ohlcv.eth-usd
	aws s3 rm --recursive s3://datasets.kamu.dev/co.alphavantage.tickers.daily.spy

push:
	kamu push net.rocketpool.reth.mint-burn --to "s3://datasets.kamu.dev/net.rocketpool.reth.mint-burn" --no-alias
	kamu push com.cryptocompare.ohlcv.eth-usd --to "s3://datasets.kamu.dev/com.cryptocompare.ohlcv.eth-usd" --no-alias
	kamu push co.alphavantage.tickers.daily.spy --to "s3://datasets.kamu.dev/co.alphavantage.tickers.daily.spy" --no-alias
