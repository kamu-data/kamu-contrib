import json
import os
import requests
import time
import random
import sys
import argparse
import datetime as dt
import itertools

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

def log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def api_request(url, **kwargs):
    log("API Request:", url, kwargs)
    resp = requests.get(url, **kwargs)
    text = resp.text
    try:
        resp.raise_for_status()
        return json.loads(text)
    except:
        log("API request failed, response body:\n" + text)
        raise


#################################
# Protocols
#################################

def protocols_list(top_n_tvl=None):
    protocols = api_request(f"https://api.llama.fi/protocols")

    if top_n_tvl:
        protocols = [p for p in protocols if p["tvl"]]
        protocols.sort(key = lambda p: p["tvl"], reverse=True)
        protocols = protocols[:args.top_n]
    else:
        protocols.sort(key = lambda c: c["name"])
    
    return protocols


def protocol_tvl(protocol):
    return api_request(f"https://api.llama.fi/protocol/{protocol}")


def protocols(args):
    for p in protocols_list(top_n_tvl = args.top_n):
        print(json.dumps(p))


def protocols_chain_tvls(args):
    protocols = protocols_list(top_n_tvl = args.top_n)
    log("Fetching chain tvls for protocols:", protocols)

    for protocol in protocols:
        data = protocol_tvl(protocol = protocol["slug"])
        for chain, chain_info in data["chainTvls"].items():
            for point in chain_info["tvl"]:
                point["protocol_slug"] = protocol["slug"]
                point["protocol_name"] = protocol["name"]
                point["chain_name"] = chain
                print(json.dumps(point))

        time.sleep(args.request_interval)


#################################
# Chains
#################################

def chains_list(top_n_tvl=None):
    chains = api_request(f"https://api.llama.fi/v2/chains")

    if top_n_tvl:
        chains = [c for c in chains if c["tvl"]]
        chains.sort(key = lambda c: c["tvl"], reverse=True)
        chains = chains[:args.top_n]
    else:
        chains.sort(key = lambda c: c["name"])
    
    return chains


def chain_tvl(chain):
    return api_request(f"https://api.llama.fi/v2/historicalChainTvl/{chain}")


def chains(args):
    for c in chains_list(top_n_tvl = args.top_n):
        print(json.dumps(c))


def chains_tvl(args):
    chains = chains_list(top_n_tvl = args.top_n)

    for c in chains:
        for point in chain_tvl(chain=c["name"]):
            point["chain_name"] = c["name"]
            print(json.dumps(point))

        time.sleep(args.request_interval)


#################################
# Pools
#################################

def pools_list(top_n_tvl=None):
    pools = api_request(
        f"https://yields.llama.fi/pools"
    )["data"]

    if top_n_tvl:
        pools = [p for p in pools if p["tvlUsd"]]
        pools.sort(key = lambda p: p["tvlUsd"], reverse=True)
        pools = pools[:args.top_n_tvl]
    else:
        pools.sort(key = lambda p: p["project"])

    return pools


def pools(args):
    for c in pools_list(top_n_tvl = args.top_n_tvl):
        print(json.dumps(c))


def pool_yield(pool):
    return api_request(
        f"https://yields.llama.fi/chart/{pool}",
    )["data"]


def pools_yield(args):
    pools = pools_list(top_n_tvl = args.top_n_tvl)

    for p in pools:
        points = pool_yield(pool=p["pool"])

        if args.enrich_with_spot_stats and len(points):
            point = points[-1]
            point["apyPct1D"] = p["apyPct1D"]
            point["apyPct7D"] = p["apyPct7D"]
            point["apyPct30D"] = p["apyPct30D"]
            point["apyMean30d"] = p["apyMean30d"]
            point["apyBaseInception"] = p["apyBaseInception"]
            point["mu"] = p["mu"]
            point["sigma"] = p["sigma"]
            point["count"] = p["count"]
            point["volumeUsd1d"] = p["volumeUsd1d"]
            point["volumeUsd7d"] = p["volumeUsd7d"]
            point["outlier"] = p["outlier"]
            point["predictions"] = json.dumps(p["predictions"])
            point["ilRisk"] = p["ilRisk"]

        for point in points:
            point["pool"] = p["pool"]
            point["project"] = p["project"]
            point["chain"] = p["chain"]
            point["symbol"] = p["symbol"]
            print(json.dumps(point))

        time.sleep(args.request_interval)


#################################
# Tokens
#################################

def tokens_list():
    with open(os.path.join(SCRIPT_DIR, 'tokens-subset.json')) as f:
        return json.load(f)["tokens"]


def tokens(args):
    for token in tokens_list():
        for chain, address in token["addresses"].items():
            print(json.dumps({
                "symbol": token["symbol"],
                "chain": chain,
                "address": address
            }))


def chunks(iterable, size):
    it = iter(iterable)
    chunk = list(itertools.islice(it, size))
    while chunk:
        yield chunk
        chunk = list(itertools.islice(it, size))


def token_prices(args):
    tokens = [
        (chain, address)
        for token in tokens_list()
        for chain, address in token["addresses"].items()
    ]

    for batch in chunks(tokens, args.batch):
        coins = ",".join(
            f"{chain}:{address}"
            for chain, address in batch
        )
        
        resp = api_request(
            f"https://coins.llama.fi/chart/{coins}", 
            params={"end": args.end, "span": args.span, "period": args.period},
        )

        for chain_addr, coin in resp["coins"].items():
            chain, address = chain_addr.split(":")

            for point in coin["prices"]:
                print(json.dumps({
                    "symbol": coin["symbol"],
                    "chain": chain,
                    "address": address,
                    "decimals": coin["decimals"],
                    "timestamp": dt.datetime.fromtimestamp(point["timestamp"], dt.timezone.utc).isoformat(),
                    "price": point["price"],
                }))

        time.sleep(args.request_interval)

#################################


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--request-interval', type=float, default=0.3)
    subparsers = parser.add_subparsers(dest='cmd', required=True)
    
    # protocols
    p_protocols = subparsers.add_parser('protocols')
    p_protocols.add_argument('--top-n', type=int, default=None)
    sp_protocols = p_protocols.add_subparsers(dest='scmd', required=False)

    p_protocols_chain_tvls = sp_protocols.add_parser('chain-tvls')
    p_protocols_chain_tvls.add_argument('--top-n', type=int, default=None)

    # chains
    p_chains = subparsers.add_parser('chains')
    p_chains.add_argument('--top-n', type=int, default=None)
    sp_chains = p_chains.add_subparsers(dest='scmd', required=False)

    p_chains_tvl = sp_chains.add_parser('tvl')
    p_chains_tvl.add_argument('--top-n', type=int, default=None)

    # pools
    p_pools = subparsers.add_parser('pools')
    p_pools.add_argument('--top-n-tvl', type=int, default=None)
    sp_pools = p_pools.add_subparsers(dest='scmd', required=False)

    p_pools_yields = sp_pools.add_parser('yield')
    p_pools_yields.add_argument('--top-n-tvl', type=int, default=None)
    p_pools_yields.add_argument('--enrich-with-spot-stats', action='store_true')

    # tokens
    p_tokens = subparsers.add_parser('tokens')
    sp_tokens = p_tokens.add_subparsers(dest='scmd', required=False)

    p_tokens_prices = sp_tokens.add_parser('prices')
    # By default we will request data with 1-day period and will align the end of the requested interval
    # with midnight UTC to ideally get the same values upon next ingestion and keep the ledger from skewing
    now_utc = dt.datetime.now(dt.timezone.utc)
    midnight_utc = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    midnight_utc = int(midnight_utc.timestamp())
    p_tokens_prices.add_argument('--end', type=int, default=midnight_utc)
    p_tokens_prices.add_argument('--span', type=int, default=365 * 3)
    p_tokens_prices.add_argument('--period', default="1d")
    p_tokens_prices.add_argument('--batch', type=int, default=1)

    
    
    args = parser.parse_args()
    log("Parsed args:", args)

    if args.cmd == 'protocols':
        if args.scmd is None:
            protocols(args)
        elif args.scmd == 'chain-tvls':
            protocols_chain_tvls(args)
    elif args.cmd == 'chains':
        if args.scmd is None:
            chains(args)
        elif args.scmd == 'tvl':
            chains_tvl(args)
    elif args.cmd == 'pools':
        if args.scmd is None:
            pools(args)
        elif args.scmd == 'yield':
            pools_yield(args)
    elif args.cmd == 'tokens':
        if args.scmd is None:
            tokens(args)
        elif args.scmd == 'prices':
            token_prices(args)