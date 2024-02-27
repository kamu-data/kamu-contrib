#!/usr/bin/env python
#
# This script initializes a graph of pipelines from dataset manifests.
# Run it from directory where you want the workspace to be created.
#
# Inputs:
# - KAMU_S3_URL - where external datasets are stored, e.g. s3://mybucket/prefix/ (note has to end with a slash)
# - KAMU_PROJECTS_ROOT - to where repository checkouts are located

import os
import sys
import json
import subprocess

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from common import *

###############################################################################

KAMU_PROJECTS_ROOT = os.environ.get("KAMU_PROJECTS_ROOT", "../../..")

###############################################################################

def get_dataset_id(name):
    res = subprocess.run("kamu list --wide --output-format json", shell=True, check=True, capture_output=True, text=True)
    for ds in json.loads(res.stdout):
        if ds["Name"] == name:
            return ds["ID"]
    raise Exception(f"Dataset {name} not found")

###############################################################################

subprocess.run(
    "kamu init",
    env=dict(
        **os.environ,
        KAMU_WORKSPACE=os.getcwd()
    ),
    shell=True,
    check=True,
)


# External datasets
for name, url in EXTERNAL_DATASETS.items():
    subprocess.run(f"kamu pull {url} --as {name}", shell=True, check=True)


# Example datasets
subprocess.run(f"kamu add -r {KAMU_PROJECTS_ROOT}/kamu-cli/examples/covid/", shell=True, check=True)
subprocess.run(f"kamu add -r {KAMU_PROJECTS_ROOT}/kamu-cli/examples/housing_prices/", shell=True, check=True)
subprocess.run(f"kamu add -r {KAMU_PROJECTS_ROOT}/kamu-cli/examples/reth-vs-snp500/", shell=True, check=True)

subprocess.run(f"kamu add -r {KAMU_PROJECTS_ROOT}/kamu-contrib/ca.bankofcanada/", shell=True, check=True)
subprocess.run(f"kamu add -r {KAMU_PROJECTS_ROOT}/kamu-contrib/com.naturalearthdata/", shell=True, check=True)
subprocess.run(f"kamu add -r {KAMU_PROJECTS_ROOT}/kamu-contrib/us.cityofnewyork.data/zipcode-boundaries.yaml", shell=True, check=True)


# Test datasets
subprocess.run(f"kamu add -r {KAMU_PROJECTS_ROOT}/kamu-contrib/testing/", shell=True, check=True)

## Derivative dataset that specified input by ID instead of name
manifest = f"""
version: 1
kind: DatasetSnapshot
content:
  name: testing.set-transform-input-by-id
  kind: Derivative
  metadata:
    - kind: SetTransform
      inputs:
        - datasetRef: {get_dataset_id("testing.empty-root")}
          alias: foo
      transform:
        kind: Sql
        engine: flink
        query: \"select event_time from foo\"
"""
subprocess.run(f"kamu add --stdin", shell=True, check=True, text=True, input=manifest)
