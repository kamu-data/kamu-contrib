#!/usr/bin/env python
#
# Just a wrapper over `kamu pull --all` that also pulls some of our uncacheable datasets.

import os
import sys
import json
import subprocess

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from common import *

###############################################################################

UNCACHEABLE_TO_PULL = [
  "account.transactions",
  "account.tokens.transfers",
  "ca.bankofcanada.exchange-rates.daily",
]

###############################################################################

# Pull uncacheables
subprocess.run(f"kamu pull {' '.join(UNCACHEABLE_TO_PULL)} --fetch-uncacheable", shell=True, check=True)

# Pull everything else
subprocess.run(f"kamu pull --all", shell=True, check=True)
