import json
import os
import requests
import time
import random
import sys
import argparse
import subprocess
import yaml

#########################################################################################

GQL_URL = "https://api.demo.kamu.dev/graphql"

def log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

#########################################################################################

def get_token():
    with open(".kamu/.kamutokenstore") as f:
        data = yaml.load(f, Loader=yaml.Loader)
    
    return data["content"][0]["tokens"][0]["accessToken"]


def list_datasets():
    return json.loads(
        subprocess.run(
            f"kamu list --wide --output-format json", 
            shell=True, check=True, capture_output=True, text=True
        ).stdout
    )

#########################################################################################

def gql_request(query):
    token = get_token()
    res = requests.post(
        GQL_URL,
        headers = {"Authorization": f"Bearer {token}"},
        json = {"query": query},
    )
    res.raise_for_status()
    res = res.json()
    if "errors" in res:
        raise Exception(f"GQL Error: {res['errors']}")
    return res


def resolve_remote_id(*, account, name):
    gql = """
    {
        datasets {
            byOwnerAndName(accountName: "{{account}}", datasetName: "{{name}}") {
                id
            }
        }
    }
    """
    resp = gql_request(
        gql.replace(
            "{{account}}", account
        ).replace(
            "{{name}}", name
        )
    )
    return (resp["data"]["datasets"]["byOwnerAndName"] or {}).get("id")


def delete_dataset(*, id):
    gql = """
    mutation {
        datasets {
            byId(datasetId: "{{id}}") {
                delete {
                    __typename
                    message
                }
            }
        }
    }

    """
    resp = gql_request(gql.replace("{{id}}", id))
    if resp["data"]["datasets"]["byId"] is None:
        raise Exception(f"Dataset {id} does not exist")
    if resp["data"]["datasets"]["byId"]["delete"]["__typename"] != "DeleteResultSuccess":
        message = resp["data"]["datasets"]["byId"]["delete"]["message"]
        raise Exception(f"Could not delete dataset {id}: {message}")

#########################################################################################

def push():
    for ds in list_datasets():
        name = ds["Name"]
        subprocess.run(
            f"kamu push {name} --to odf+https://api.demo.kamu.dev/kamu/{name}",
            shell=True, check=True
        )


# TODO: fetch-uncacheable
def update():
    token = get_token()

    gql = """
    mutation {
        datasets {
            byId(datasetId: "{{id}}") {
                flows {
                    runs {
                        triggerFlow(datasetFlowType: INGEST) {
                            __typename
                        }
                    }
                }
            }
        }
    }
    """

    for ds in list_datasets():
        print("Triggering update:", ds["Name"], ds["ID"])
        gql_request(gql.replace("{{id}}", ds["ID"]))


def configure():
    request_interval = 2
    top_n = 100
    variables = {
        "com.defillama.chains.tvl": [
            ("request_interval", request_interval),
            ("top_n_chains", top_n),
        ],
        "com.defillama.protocols.chain-tvls": [
            ("request_interval", request_interval),
            ("top_n_protocols", top_n),
        ],
        "com.defillama.pools.yield": [
            ("request_interval", request_interval),
            ("top_n_pools", top_n),
        ],
    }

    gql = """
    mutation {
        datasets {
            byId(datasetId: "{{id}}") {
                envVars {
                    saveEnvVariable(key: "{{key}}", value: "{{value}}", isSecret: false) {
                        __typename
                    }
                }
            }
        }
    }
    """

    ds_name_to_id = {
        ds["Name"]: ds["ID"]
        for ds in list_datasets()
    }

    for name, vars in variables.items():
        id = ds_name_to_id[name]
        for key, value in vars:
            print(f"For {name} configuring: {key}={value}")
            gql_request(
                gql.replace(
                    "{{id}}", id
                ).replace(
                    "{{key}}", key
                ).replace(
                    "{{value}}", str(value)
                )
            )


def delete():
    for ds in list_datasets():
        # local datasets may not have the same identity as remote
        account = "kamu"
        name = ds["Name"]
        remote_id = resolve_remote_id(account=account, name=name)
        if remote_id is None:
            print(f"Dataset {account}/{name} does not exist in repo")
            continue
        print(f"Deleting dataset {account}/{name} ({remote_id})")
        delete_dataset(id=remote_id)

#########################################################################################

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    cmd = parser.add_subparsers(dest='cmd', required=True)
    
    cmd_push = cmd.add_parser('push')

    cmd_configure = cmd.add_parser('configure')

    cmd_update = cmd.add_parser('update')

    cmd_delete = cmd.add_parser('delete')
    
    args = parser.parse_args()
    log("Parsed args:", args)

    if args.cmd == 'push':
        push()
    elif args.cmd == 'configure':
        configure()
    elif args.cmd == 'update':
        update()
    elif args.cmd == 'delete':
        delete()
