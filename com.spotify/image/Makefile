IMAGE = ghcr.io/kamu-data/fetch-com.spotify:0.1.0

.PHONY: requirements
requirements:
	pip-compile requirements.in

.PHONY: image
image:
	docker build -t $(IMAGE) .


.PHONY: image-push
image-push:
	docker push $(IMAGE)
