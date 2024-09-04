#!/usr/bin/env python

# Expects PINATA_ACCESS_TOKEN env var to be set

import os
import argparse
import requests
import json


PINATA_API_URL = 'https://api.pinata.cloud'


def access_token():
    token = os.environ.get('PINATA_ACCESS_TOKEN')
    if token is None:
        raise Exception('PINATA_ACCESS_TOKEN env var was not provided')
    return token


def headers():
    return {
        'Authorization': f'Bearer {access_token()}'
    }


def unpin_old(name, keep_latest):
    resp = requests.get(f'{PINATA_API_URL}/data/pinList', headers=headers(), params={
        'pageLimit': 1000,
        'status': 'pinned',
    })
    resp.raise_for_status()
    resp = resp.json()

    print("Total pins returned:", len(resp["rows"]))

    entries_by_name = {}
    for row in resp['rows']:
        entry_name = row['metadata']['name']

        if name is not None and entry_name != name:
            continue

        if row['date_unpinned'] is not None:
            continue

        entries = entries_by_name.setdefault(entry_name, [])
        entries.append(row)

    print(f"Found active pins:", len(entries_by_name))

    for name, entries in entries_by_name.items():
        entries.sort(key=lambda e: e['date_pinned'], reverse=True)

        to_remove = entries[keep_latest:]
        for entry in to_remove:
            cid = entry['ipfs_pin_hash']
            date = entry['date_pinned']

            print(f"Unpinning {name} {cid} {date}")
            requests.delete(f'{PINATA_API_URL}/pinning/unpin/{cid}', headers=headers()).raise_for_status()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    foo_parser = subparsers.add_parser('unpin-old')
    foo_parser.add_argument('--name')
    foo_parser.add_argument('--keep-latest', type=int, default=0)
    args = parser.parse_args()
    if args.command == 'unpin-old':
        unpin_old(name=args.name, keep_latest=args.keep_latest)
    else:
        parser.print_help()
