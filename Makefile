KAMU_WORKSPACE=.priv/workspace-contrib
DATE:=$(shell date +%F)
S3_CONTRIB_BASE_URL=s3://datasets.kamu.dev/odf/v2/contrib/
S3_BACKUP_BASE_URL=s3://datasets.kamu.dev/odf/backup/v2/contrib/

###############################################################################
# Repo maintenance
###############################################################################

.PHONY: strip-notebooks
strip-notebooks:
	find . -name '.ipynb_checkpoints' -type d -prune -exec rm -rf {} \;
	find . -name '*.ipynb' -type f -exec nbstripout {} \;


###############################################################################
# Datasets upkeep
###############################################################################

.PHONY: local-compact-hard
local-compact-hard:
	KAMU_WORKSPACE=$(KAMU_WORKSPACE) kamu system compact --hard "net.rocketpool.reth.tokens-minted"
	KAMU_WORKSPACE=$(KAMU_WORKSPACE) kamu system compact --hard "net.rocketpool.reth.tokens-burned"
	KAMU_WORKSPACE=$(KAMU_WORKSPACE) kamu system compact --hard "com.cryptocompare.ohlcv.eth-usd"
	KAMU_WORKSPACE=$(KAMU_WORKSPACE) kamu system compact --hard "co.alphavantage.tickers.daily.spy"


.PHONY: local-pull
local-pull:
	KAMU_WORKSPACE=$(KAMU_WORKSPACE) kamu pull --all --fetch-uncacheable


###############################################################################
# S3
###############################################################################

.PHONY: s3-backup
s3-backup:
	aws s3 cp --recursive "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.tokens-minted" "$(S3_BACKUP_BASE_URL)net.rocketpool.reth.tokens-minted.$(DATE)"
	aws s3 cp --recursive "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.tokens-burned" "$(S3_BACKUP_BASE_URL)net.rocketpool.reth.tokens-burned.$(DATE)"
	aws s3 cp --recursive "$(S3_CONTRIB_BASE_URL)com.cryptocompare.ohlcv.eth-usd" "$(S3_BACKUP_BASE_URL)com.cryptocompare.ohlcv.eth-usd.$(DATE)"
	aws s3 cp --recursive "$(S3_CONTRIB_BASE_URL)co.alphavantage.tickers.daily.spy" "$(S3_BACKUP_BASE_URL)co.alphavantage.tickers.daily.spy.$(DATE)"


.PHONY: s3-purge
s3-purge:
	aws s3 rm --recursive "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.tokens-minted"
	aws s3 rm --recursive "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.tokens-burned"
	aws s3 rm --recursive "$(S3_CONTRIB_BASE_URL)com.cryptocompare.ohlcv.eth-usd"
	aws s3 rm --recursive "$(S3_CONTRIB_BASE_URL)co.alphavantage.tickers.daily.spy"

.PHONY: sync-from-s3
sync-from-s3:
	mkdir -p $(KAMU_WORKSPACE)
	KAMU_WORKSPACE=$(KAMU_WORKSPACE) kamu init --exists-ok
	KAMU_WORKSPACE=$(KAMU_WORKSPACE) kamu pull "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.tokens-minted"
	KAMU_WORKSPACE=$(KAMU_WORKSPACE) kamu pull "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.tokens-burned"
	KAMU_WORKSPACE=$(KAMU_WORKSPACE) kamu pull "$(S3_CONTRIB_BASE_URL)com.cryptocompare.ohlcv.eth-usd"
	KAMU_WORKSPACE=$(KAMU_WORKSPACE) kamu pull "$(S3_CONTRIB_BASE_URL)co.alphavantage.tickers.daily.spy"

.PHONY: sync-to-s3
sync-to-s3:
	KAMU_WORKSPACE=$(KAMU_WORKSPACE) kamu push net.rocketpool.reth.tokens-minted --to "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.tokens-minted" --no-alias
	KAMU_WORKSPACE=$(KAMU_WORKSPACE) kamu push net.rocketpool.reth.tokens-burned --to "$(S3_CONTRIB_BASE_URL)net.rocketpool.reth.tokens-burned" --no-alias
	KAMU_WORKSPACE=$(KAMU_WORKSPACE) kamu push com.cryptocompare.ohlcv.eth-usd --to "$(S3_CONTRIB_BASE_URL)com.cryptocompare.ohlcv.eth-usd" --no-alias
	KAMU_WORKSPACE=$(KAMU_WORKSPACE) kamu push co.alphavantage.tickers.daily.spy --to "$(S3_CONTRIB_BASE_URL)co.alphavantage.tickers.daily.spy" --no-alias


###############################################################################
# IPFS
###############################################################################

.PHONY: push-ipfs
push-ipfs:
	.ci/push-to-ipfs.sh net.rocketpool.reth.tokens-minted
	.ci/push-to-ipfs.sh net.rocketpool.reth.tokens-burned
	.ci/push-to-ipfs.sh com.cryptocompare.ohlcv.eth-usd
	.ci/push-to-ipfs.sh co.alphavantage.tickers.daily.spy
