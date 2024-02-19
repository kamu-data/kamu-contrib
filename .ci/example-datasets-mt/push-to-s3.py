#!/usr/bin/env python

import os
import sys
import json
import subprocess

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from common import *

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

    url = f"{S3_EXAMPLE_MT_DATASETS_URL}{id}/"

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
