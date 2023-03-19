IMAGE = ghcr.io/kamu-data/fetch-com.coinpaprika.tickers.eth-usd:0.1.0

.PHONY: image
image:
	docker build -t $(IMAGE) .


.PHONY: image-push
image-push:
	docker push $(IMAGE)
