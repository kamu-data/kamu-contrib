DATE:=$(shell date +%F)
S3_CONTRIB_BASE_URL=s3://datasets.kamu.dev/odf/v2/contrib/
S3_BACKUP_BASE_URL=s3://datasets.kamu.dev/odf/backup/v2/contrib/


###############################################################################
# Datasets upkeep
###############################################################################

.PHONY: init-from-manifests
init-from-manifests:
	kamu init --exists-ok
	kamu add ../../net.rocketpool/reth.tokens-minted.yaml
	kamu add ../../net.rocketpool/reth.tokens-burned.yaml
	kamu add ../../com.cryptocompare/ohlcv.eth-usd.yaml
	kamu add ../../co.alphavantage/tickers.daily.spy.yaml

	kamu add ../../com.github/com.github.*

	kamu add ../../com.youtube/com.youtube.*


.PHONY: init-from-s3
init-from-s3:
	kamu init --exists-ok
	kamu pull "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.tokens-minted"
	kamu pull "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.tokens-burned"
	kamu pull "$(S3_CONTRIB_BASE_URL)com.cryptocompare.ohlcv.eth-usd"
	kamu pull "$(S3_CONTRIB_BASE_URL)co.alphavantage.tickers.daily.spy"

	kamu pull "$(S3_CONTRIB_BASE_URL)com.github.kamu-data.clones"
	kamu pull "$(S3_CONTRIB_BASE_URL)com.github.kamu-data.stargazers"
	kamu pull "$(S3_CONTRIB_BASE_URL)com.github.kamu-data.views"

	kamu pull "$(S3_CONTRIB_BASE_URL)com.youtube.channel.kamu-data.stats"
	kamu pull "$(S3_CONTRIB_BASE_URL)com.youtube.channel.kamu-data.videos.stats"
	kamu pull "$(S3_CONTRIB_BASE_URL)com.youtube.playlist.featuring-kamu-data.videos.stats"


.PHONY: local-compact-hard
local-compact-hard:
	kamu system compact --hard "net.rocketpool.reth.tokens-minted"
	kamu system compact --hard "net.rocketpool.reth.tokens-burned"
	kamu system compact --hard "com.cryptocompare.ohlcv.eth-usd"
	kamu system compact --hard "co.alphavantage.tickers.daily.spy"

	kamu system compact --hard "com.github.kamu-data.clones"
	kamu system compact --hard "com.github.kamu-data.stargazers"
	kamu system compact --hard "com.github.kamu-data.views"

	kamu system compact --hard "com.youtube.channel.kamu-data.stats"
	kamu system compact --hard "com.youtube.channel.kamu-data.videos.stats"
	kamu system compact --hard "com.youtube.playlist.featuring-kamu-data.videos.stats"


###############################################################################
# S3
###############################################################################

.PHONY: s3-backup
s3-backup:
	aws s3 cp --recursive "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.tokens-minted" "$(S3_BACKUP_BASE_URL)net.rocketpool.reth.tokens-minted.$(DATE)"
	aws s3 cp --recursive "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.tokens-burned" "$(S3_BACKUP_BASE_URL)net.rocketpool.reth.tokens-burned.$(DATE)"
	aws s3 cp --recursive "$(S3_CONTRIB_BASE_URL)com.cryptocompare.ohlcv.eth-usd" "$(S3_BACKUP_BASE_URL)com.cryptocompare.ohlcv.eth-usd.$(DATE)"
	aws s3 cp --recursive "$(S3_CONTRIB_BASE_URL)co.alphavantage.tickers.daily.spy" "$(S3_BACKUP_BASE_URL)co.alphavantage.tickers.daily.spy.$(DATE)"

	aws s3 cp --recursive "$(S3_CONTRIB_BASE_URL)com.github.kamu-data.clones" "$(S3_BACKUP_BASE_URL)com.github.kamu-data.clones.$(DATE)"
	aws s3 cp --recursive "$(S3_CONTRIB_BASE_URL)com.github.kamu-data.stargazers" "$(S3_BACKUP_BASE_URL)com.github.kamu-data.stargazers.$(DATE)"
	aws s3 cp --recursive "$(S3_CONTRIB_BASE_URL)com.github.kamu-data.views" "$(S3_BACKUP_BASE_URL)com.github.kamu-data.views.$(DATE)"

	aws s3 cp --recursive "$(S3_CONTRIB_BASE_URL)com.youtube.channel.kamu-data.stats" "$(S3_BACKUP_BASE_URL)com.youtube.channel.kamu-data.stats.$(DATE)"
	aws s3 cp --recursive "$(S3_CONTRIB_BASE_URL)com.youtube.channel.kamu-data.videos.stats" "$(S3_BACKUP_BASE_URL)com.youtube.channel.kamu-data.videos.stats.$(DATE)"
	aws s3 cp --recursive "$(S3_CONTRIB_BASE_URL)com.youtube.playlist.featuring-kamu-data.videos.stats" "$(S3_BACKUP_BASE_URL)com.youtube.playlist.featuring-kamu-data.videos.stats.$(DATE)"


.PHONY: s3-purge
s3-purge:
	aws s3 rm --recursive "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.tokens-minted"
	aws s3 rm --recursive "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.tokens-burned"
	aws s3 rm --recursive "$(S3_CONTRIB_BASE_URL)com.cryptocompare.ohlcv.eth-usd"
	aws s3 rm --recursive "$(S3_CONTRIB_BASE_URL)co.alphavantage.tickers.daily.spy"

	aws s3 rm --recursive "$(S3_CONTRIB_BASE_URL)com.github.kamu-data.clones"
	aws s3 rm --recursive "$(S3_CONTRIB_BASE_URL)com.github.kamu-data.stargazers"
	aws s3 rm --recursive "$(S3_CONTRIB_BASE_URL)com.github.kamu-data.views"

	aws s3 rm --recursive "$(S3_CONTRIB_BASE_URL)com.youtube.channel.kamu-data.stats"
	aws s3 rm --recursive "$(S3_CONTRIB_BASE_URL)com.youtube.channel.kamu-data.videos.stats"
	aws s3 rm --recursive "$(S3_CONTRIB_BASE_URL)com.youtube.playlist.featuring-kamu-data.videos.stats"


.PHONY: s3-push
s3-push:
	kamu push net.rocketpool.reth.tokens-minted --to "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.tokens-minted" --no-alias
	kamu push net.rocketpool.reth.tokens-burned --to "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.tokens-burned" --no-alias
	kamu push com.cryptocompare.ohlcv.eth-usd --to "$(S3_CONTRIB_BASE_URL)com.cryptocompare.ohlcv.eth-usd" --no-alias
	kamu push co.alphavantage.tickers.daily.spy --to "$(S3_CONTRIB_BASE_URL)co.alphavantage.tickers.daily.spy" --no-alias

	kamu push com.github.kamu-data.clones --to "$(S3_CONTRIB_BASE_URL)com.github.kamu-data.clones"
	kamu push com.github.kamu-data.stargazers --to "$(S3_CONTRIB_BASE_URL)com.github.kamu-data.stargazers"
	kamu push com.github.kamu-data.views --to "$(S3_CONTRIB_BASE_URL)com.github.kamu-data.views"

	kamu push com.youtube.channel.kamu-data.stats --to "$(S3_CONTRIB_BASE_URL)com.youtube.channel.kamu-data.stats"
	kamu push com.youtube.channel.kamu-data.videos.stats --to "$(S3_CONTRIB_BASE_URL)com.youtube.channel.kamu-data.videos.stats"
	kamu push com.youtube.playlist.featuring-kamu-data.videos.stats --to "$(S3_CONTRIB_BASE_URL)com.youtube.playlist.featuring-kamu-data.videos.stats"
