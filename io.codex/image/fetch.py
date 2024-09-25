import json
import os
import requests
import time
import random
import sys
import argparse
import datetime as dt
import itertools


TOKEN = os.environ["CODEX_API_KEY"]
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def api_request(gql, variables=None):
    log("API Request:", gql, variables)
    resp = requests.post(
        "https://graph.codex.io/graphql",
        headers = {"Authorization": TOKEN},
        json = {
            "query": gql,
            "variables": variables or {},
        },
    )
    text = resp.text
    try:
        resp.raise_for_status()
        data = json.loads(text)
        if "errors" in data:
            raise Exception(f"GQL Error: {res['errors']}")
        return data
    except:
        log("API request failed, response body:\n" + text)
        raise

#################################
# Tokens
#################################

def tokens_list():
    with open(os.path.join(SCRIPT_DIR, 'tokens-subset.json')) as f:
        return json.load(f)["tokens"]


# Resolves network IDs for predefined token subset
def tokens_list_resolved():
    networks = api_request("""
    query {
        getNetworks {
            id
            name
        }
    }
    """)["data"]["getNetworks"]

    network_name_to_id = {n["name"]: n["id"] for n in networks}

    return [
        {
            "symbol": token["symbol"],
            "network_id": network_name_to_id[network],
            "network_name": network,
            "address": address,
        }
        for token in tokens_list()
        for network, address in token["addresses"].items()
    ]


def tokens_bars(args):
    t_from = int(dt.datetime.fromisoformat(getattr(args, "from")).timestamp())
    t_to = int(dt.datetime.fromisoformat(args.to).timestamp())

    tokens = tokens_list_resolved()

    gql = """
    query($symbol: String!, $from: Int!, $to: Int!, $resolution: String!) {
        getBars(
            symbol: $symbol
            from: $from
            to: $to
            resolution: $resolution
            removeLeadingNullValues: true
        ) {
            t
            o
            l
            h
            c
            transactions
            volume
            buys
            buyers
            buyVolume
            sells
            sellers
            sellVolume
        }
    }
    """

    for token in tokens:
        resp = api_request(gql, variables={
            "symbol": "{address}:{network_id}".format(**token),
            "from": t_from,
            "to": t_to,
            "resolution": args.resolution
        })["data"]["getBars"]

        assert (
            len(resp["t"]) ==
            len(resp["o"]) ==
            len(resp["l"]) ==
            len(resp["h"]) ==
            len(resp["c"]) ==
            len(resp["transactions"]) ==
            len(resp["volume"]) ==
            len(resp["buys"]) ==
            len(resp["buyers"]) ==
            len(resp["buyVolume"]) ==
            len(resp["sells"]) ==
            len(resp["sellers"]) ==
            len(resp["sellVolume"])
        )

        for (
            t,
            o,
            l,
            h,
            c,
            transactions,
            volume,
            buys,
            buyers,
            buyVolume,
            sells,
            sellers,
            sellVolume
        ) in zip(
            resp["t"],
            resp["o"],
            resp["l"],
            resp["h"],
            resp["c"],
            resp["transactions"],
            resp["volume"],
            resp["buys"],
            resp["buyers"],
            resp["buyVolume"],
            resp["sells"],
            resp["sellers"],
            resp["sellVolume"],
        ):
            point = {
                "event_time": dt.datetime.fromtimestamp(t, dt.timezone.utc).isoformat(),
                "symbol": token["symbol"],
                "network_id": token["network_id"],
                "network_name": token["network_name"],
                "address": token["address"],
                "open": o,
                "low": l,
                "high": h,
                "close": c,
                "transactions": transactions,
                "volume": volume,
                "buys": buys,
                "buyers": buyers,
                "buy_volume": buyVolume,
                "sells": sells,
                "sellers": sellers,
                "sell_volume": sellVolume,
            }

            print(json.dumps(point))

        time.sleep(args.request_interval)

#################################


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--request-interval', type=float, default=0.3)
    subparsers = parser.add_subparsers(dest='cmd', required=True)
    
    # tokens
    p_tokens = subparsers.add_parser('tokens')
    sp_tokens = p_tokens.add_subparsers(dest='scmd', required=True)

    p_tokens_bars = sp_tokens.add_parser('bars')
    # By default we will request data with 1-day period and will align the end of the requested interval
    # with midnight UTC to ideally get the same values upon next ingestion and keep the ledger from skewing
    p_tokens_bars.add_argument('--from', type=str, default='2022-01-01:00:00:00Z')
    p_tokens_bars.add_argument('--to', type=str, default=dt.datetime.now(dt.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).isoformat())
    p_tokens_bars.add_argument('--resolution', default="1D")
    
    args = parser.parse_args()
    log("Parsed args:", args)

    if args.cmd == 'tokens':
        if args.scmd == 'bars':
            tokens_bars(args)
