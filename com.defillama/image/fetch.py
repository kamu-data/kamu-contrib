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


def get_last_updated():
    last_updated = os.environ.get('ODF_ETAG')
    if last_updated:
        return dt.datetime.fromisoformat(last_updated)
    else:
        return None


def write_last_updated(last_updated):
    etag_path = os.environ.get("ODF_NEW_ETAG_PATH")
    if etag_path:
        with open(etag_path, 'w') as f:
            f.write(last_updated.isoformat())


def is_up_to_date(last_updated, now):
    if last_updated:
        delta = now - last_updated
        log("Time since last update:", delta)
        if delta.days < 1:
            log("Considering up-to-date")
            write_last_updated(last_updated)
            return True
    return False


def write_has_more():
    path = os.environ.get("ODF_NEW_HAS_MORE_DATA_PATH")
    if path:
        with open(path, 'w') as f:
            pass


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
    now = dt.datetime.now(dt.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    last_updated = get_last_updated()
    if is_up_to_date(last_updated, now):
        return

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

    write_last_updated(now)


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
    now = dt.datetime.now(dt.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    last_updated = get_last_updated()
    if is_up_to_date(last_updated, now):
        return

    chains = chains_list(top_n_tvl = args.top_n)

    for c in chains:
        for point in chain_tvl(chain=c["name"]):
            point["chain_name"] = c["name"]
            print(json.dumps(point))

        time.sleep(args.request_interval)

    write_last_updated(now)


#################################
# Pools
#################################

def predefined_pools():
    with open(os.path.join(SCRIPT_DIR, "pools-subset.json")) as f:
        return json.load(f)["pools"]

def pools_list(top_n_tvl=None, predefined_subset=False):
    pools = api_request(
        f"https://yields.llama.fi/pools"
    )["data"]

    if top_n_tvl:
        pools = [p for p in pools if p["tvlUsd"]]
        pools.sort(key = lambda p: p["tvlUsd"], reverse=True)
        pools = pools[:args.top_n_tvl]
    elif predefined_subset:
        predefined = {
            p["pool"]: p
            for p in predefined_pools()
        }
        
        pools = [
            p for p in pools
            if p["pool"] in predefined
        ]
        assert len(predefined) == len(pools)

        for p in pools:
            p["underlyingTokenSymbols"] = predefined[p["pool"]]["underlyingTokenSymbols"]

        pools.sort(key = lambda p: p["project"])
    else:
        pools.sort(key = lambda p: p["project"])

    return pools


def pools(args):
    for c in pools_list(top_n_tvl = args.top_n_tvl, predefined_subset = args.predefined_subset):
        print(json.dumps(c))


def pool_yield(pool):
    return api_request(
        f"https://yields.llama.fi/chart/{pool}",
    )["data"]


def pools_yield(args):
    now = dt.datetime.now(dt.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    last_updated = get_last_updated()
    if is_up_to_date(last_updated, now):
        return

    pools = pools_list(top_n_tvl = args.top_n_tvl, predefined_subset = args.predefined_subset)

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
            point["poolMeta"] = p["poolMeta"]
            print(json.dumps(point))

        time.sleep(args.request_interval)

    write_last_updated(now)


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
    # Align to midnight to make sure we don't ingest data that might still be updated
    now = dt.datetime.now(dt.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    now_ts = now.timestamp()

    last_updated = get_last_updated()
    if is_up_to_date(last_updated, now):
        return

    if not last_updated:
        last_updated = dt.datetime.fromisoformat(args.start)

    est_data_points = (now - last_updated).days
    has_more = False
    if est_data_points > args.span:
        now = last_updated + dt.timedelta(days = args.span)
        has_more = True

    log(f"Ingest iteration start: {last_updated.isoformat()}, end: {now.isoformat()}, span: {args.span}, estimated: {est_data_points}, has_more: {has_more}")

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
            params={"start": last_updated.timestamp(), "span": args.span, "period": args.period},
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

    write_last_updated(now)
    if has_more:
        write_has_more()

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
    p_pools.add_argument('--predefined-subset', action='store_true')
    sp_pools = p_pools.add_subparsers(dest='scmd', required=False)

    p_pools_yields = sp_pools.add_parser('yield')
    p_pools_yields.add_argument('--top-n-tvl', type=int, default=None)
    p_pools_yields.add_argument('--predefined-subset', action='store_true')
    p_pools_yields.add_argument('--enrich-with-spot-stats', action='store_true')

    # tokens
    p_tokens = subparsers.add_parser('tokens')
    sp_tokens = p_tokens.add_subparsers(dest='scmd', required=False)

    p_tokens_prices = sp_tokens.add_parser('prices')
    p_tokens_prices.add_argument('--start', type=str, default='2021-01-01:00:00:00Z')
    p_tokens_prices.add_argument('--span', type=int, default=365)
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