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

KAMU_S3_URL=os.environ["KAMU_S3_URL"]

###############################################################################

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

subprocess.run("kamu init", shell=True, check=True)

for id in s3_datasets:
    flags = ""
    if not is_external(id):
        flags = "--no-alias"
    
    subprocess.run(
        f"kamu pull {KAMU_S3_URL}{id} {flags}", 
        shell=True,
        check=True,
    )
