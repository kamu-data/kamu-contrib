#!/usr/bin/env python
#
# This script pulls datasets from S3 bucket.
#
# Inputs:
# - KAMU_S3_URL - where external datasets are stored, e.g. s3://mybucket/prefix/ (note has to end with a slash)

import os
import sys
import subprocess

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from common import *

###############################################################################

KAMU_S3_URL = os.environ.get("KAMU_S3_URL", S3_EXAMPLE_DATASETS_URL)

###############################################################################

subprocess.run("kamu init --exists-ok", shell=True, check=True)

# External datasets
for name, url in EXTERNAL_DATASETS.items():
    subprocess.run(f"kamu pull {url} --as {name}", shell=True, check=True)

# Regular datasets
s3_datasets = [
    line.strip().split(' ')[1].rstrip("/")
    for line in subprocess.run(
        f"aws s3 ls {KAMU_S3_URL}",
        shell=True,
        text=True,
        check=True,
        capture_output=True,
    ).stdout.splitlines()
]

for name in s3_datasets:
    subprocess.run(
        f"kamu -v pull --no-alias {KAMU_S3_URL}{name}",
        shell=True,
        check=True,
    )
