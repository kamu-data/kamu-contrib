IMAGE = ghcr.io/kamu-data/fetch-net.rocketpool.reth.mint-burn:0.1.1

.PHONY: image
image:
	docker build -t $(IMAGE) .


.PHONY: image-push
image-push:
	docker push $(IMAGE)


.PHONY: test
test:
	# Expects ETH_NODE_PROVIDER_URL env var to be set
	ODF_ETAG="17678995" \
	npm run start
