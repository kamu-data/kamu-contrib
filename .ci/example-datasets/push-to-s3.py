#!/usr/bin/env python
#
# This script pushes updated datasets into S3.
#
# Inputs:
# - KAMU_S3_URL - where external datasets are stored, e.g. s3://mybucket/prefix/ (note has to end with a slash)

import os
import sys
import json
import subprocess

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from common import *

###############################################################################

KAMU_S3_URL = os.environ.get("KAMU_S3_URL", S3_EXAMPLE_DATASETS_URL)

###############################################################################

datasets = [
    ds["Name"]
    for ds in json.loads(
        subprocess.run(
            f"kamu list --output-format json", 
            shell=True, check=True, capture_output=True, text=True
        ).stdout
    )
]

for name in datasets:
    if is_external(name):
        continue
    
    subprocess.run(
        f"kamu push {name} --to {KAMU_S3_URL}{name} --no-alias", 
        shell=True, check=True
    )
