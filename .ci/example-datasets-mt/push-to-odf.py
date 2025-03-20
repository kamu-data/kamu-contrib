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
PLATFORM_TOKEN = os.environ.get('PLATFORM_TOKEN', None)
PUSH_FLAGS = os.environ.get('PUSH_FLAGS', '')

###############################################################################

# List datasets
datasets = json.loads(subprocess.check_output(
    "kamu list --all-accounts --output-format json --wide",
    shell=True,
))

# Login to Platform service as an admin account
subprocess.run(
    f"kamu --account {PLATFORM_LOGIN} login {PLATFORM_API_URL} --access-token {PLATFORM_TOKEN}",
    shell=True,
    check=True,
)

# Push to Platform via ODF Smart Transfer Protocol
for dataset in datasets:
    account = dataset["Owner"]
    name = dataset["Name"]

    # Form odf+https URL for the dataset
    url = f"odf+{PLATFORM_API_URL}/{account}/{name}/"

    # Push via Smart Transfer Protocol:
    #  - log as a local account (who has logged in to the Platform and has valid token)
    #  - use target account name to properly identify the dataset
    subprocess.run(
        f"kamu --account {PLATFORM_LOGIN} push {PUSH_FLAGS} {account}/{name} --to {url}",
        shell=True,
        check=True,
    )
