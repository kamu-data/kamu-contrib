IMAGE = ghcr.io/kamu-data/fetch-net.rocketpool.reth.mint-burn:0.2.0

.PHONY: image
image:
	docker build -t $(IMAGE) .


.PHONY: image-push
image-push:
	docker push $(IMAGE)


.PHONY: test
test:
	# Expects ETH_NODE_PROVIDER_URL env var to be set
	ODF_ETAG=0 \
	BLOCK_BATCH_SIZE=100000 \
	ODF_BATCH_SIZE=100000 \
	ODF_NEW_ETAG_PATH=.odf_new_etag \
	ODF_NEW_HAS_MORE_DATA_PATH=.odf_new_has_more \
		npm run start
