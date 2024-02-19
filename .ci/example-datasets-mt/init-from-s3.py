#!/usr/bin/env python

import os
import sys
import subprocess

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from common import *

###############################################################################

subprocess.run(
    "kamu init --multi-tenant --exists-ok", 
    env=dict(
        **os.environ,
        KAMU_WORKSPACE=os.getcwd()
    ),
    shell=True,
    check=True,
)

# Datasets owned by `kamu`
s3_datasets = []
for base_url in [S3_CONTRIB_DATASETS_URL, S3_EXAMPLE_DATASETS_URL]:
    s3_datasets.extend(
        base_url + d
        for d in s3_listdir(base_url)
    )

for url in s3_datasets:
    subprocess.run(
        f"kamu --account kamu pull --no-alias {url}",
        shell=True,
        check=True,
    )

# Multi-tenant datasets
for did in s3_listdir(S3_EUROPORT_REPO_URL):
    url = S3_EUROPORT_REPO_URL + did
    alias = s3_cat(f"{S3_EUROPORT_REPO_URL}{did}info/alias")
    account, name = alias.split('/', 1)
    subprocess.run(
        f"kamu --account {account} pull --no-alias {url} --as {name}",
        shell=True,
        check=True,
    )
