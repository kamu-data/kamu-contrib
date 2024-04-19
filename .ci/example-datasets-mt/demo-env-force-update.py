#!/usr/bin/env python

import os
import sys
import subprocess
import json

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from common import *

###############################################################################

S3_DEMO_REPO_URL = "s3://repo.demo.stg.kamu.dev.us-west-2/"

###############################################################################

def list_datasets_in_s3(repo_url):
    for did in s3_listdir(repo_url):
        url = repo_url + did
        alias = s3_cat(f"{repo_url}{did}info/alias")
        account, name = alias.split('/', 1)
        yield url, did, account, name

def push_local_dataset_to_s3(dataset, repo_url):
    id = dataset["ID"].removeprefix("did:odf:")
    account = dataset["Owner"]
    name = dataset["Name"]

    url = f"{repo_url}{id}/"

    subprocess.run(
        f"kamu --account {account} push {name} --to {url}",
        shell=True,
        check=True,
    )

    # Set account and alias
    subprocess.run(
        f"aws s3 cp - {url}info/alias",
        input=f"{account}/{name}".encode("utf8"),
        shell=True,
        check=True,
    )


# List local datasets
local_datasets = {
    (ds["Owner"], ds["Name"]): ds
    for ds in json.loads(subprocess.check_output(
        "kamu list --all-accounts --output-format json --wide",
        shell=True,
    ))
}

# Replace remote datasets of matching names with local versions, keeping the others
for (remote_ds_url, did, account, name) in list_datasets_in_s3(S3_DEMO_REPO_URL):
    local_dataset = local_datasets.get((account, name))
    if local_dataset is not None:
        print(f">>> Deleting {account}/{name} ({did})")
        subprocess.run(
            f"aws s3 rm --recursive {remote_ds_url}",
            input=f"{account}/{name}".encode("utf8"),
            shell=True,
            check=True,
        )
        new_id = local_dataset["ID"]
        print(f">>> Pushing {account}/{name} ({new_id})")
        push_local_dataset_to_s3(local_dataset, S3_DEMO_REPO_URL)
    else:
        print(f">>> Keeping {account}/{name} ({did})")