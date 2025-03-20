#!/usr/bin/env python

import os
import sys
import json
import subprocess

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from common import *

###############################################################################

PLATFORM_API_URL = os.environ.get('PLATFORM_API_URL', None)
PLATFORM_LOGIN = os.environ.get('PLATFORM_LOGIN', None)
PLATFORM_PASSWORD = os.environ.get('PLATFORM_PASSWORD', None)
PUSH_FLAGS = os.environ.get('PUSH_FLAGS', '')

###############################################################################

def get_password(account: str) -> str:
    return PLATFORM_PASSWORD if account == PLATFORM_LOGIN else account

###############################################################################

# List datasets
datasets = json.loads(subprocess.check_output(
    "kamu list --all-accounts --output-format json --wide",
    shell=True,
))

# Push to s3
for dataset in datasets:
    id = dataset["ID"].removeprefix("did:odf:")
    account = dataset["Owner"]
    name = dataset["Name"]

    # Login to Platform service as a target account
    subprocess.run(
        f"kamu --account {account} login password {account} {get_password(account)} {PLATFORM_API_URL}",
        shell=True,
        check=True,
    )

    # Form odf+https URL for the dataset
    url = f"odf+{PLATFORM_API_URL}/{account}/{name}/"

    # Push via Smart Transfer Protocol
    subprocess.run(
        f"kamu --account {account} push {PUSH_FLAGS} {name} --to {url}",
        shell=True,
        check=True,
    )
