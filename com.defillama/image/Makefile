IMAGE = ghcr.io/kamu-data/fetch-com.defillama:0.3.0

.PHONY: requirements
requirements:
	pip-compile requirements.in

.PHONY: image
image:
	docker build -t $(IMAGE) .


.PHONY: image-push
image-push:
	docker push $(IMAGE)
