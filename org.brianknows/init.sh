#!/bin/sh

kamu init --exists-ok

kamu repo add demo "odf+https://api.demo.kamu.dev" || true

# Pull root datasets
kamu pull demo/kamu/com.defillama.chains
kamu pull demo/kamu/com.defillama.chains.tvl
kamu pull demo/kamu/com.defillama.pools
kamu pull demo/kamu/com.defillama.pools.yield
kamu pull demo/kamu/com.defillama.protocols
kamu pull demo/kamu/com.defillama.protocols.chain-tvls
kamu pull demo/kamu/com.defillama.tokens.prices
kamu pull demo/kamu/io.codex.tokens.olhcv

kamu add . -r
