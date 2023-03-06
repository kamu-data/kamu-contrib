import json
import os
import requests

user = os.environ["GH_USER"]
repo = os.environ["GH_REPO"]
per_page = int(os.environ.get("GH_PER_PAGE", "100"))

#etag = os.environ.get("ODF_ETAG")
#new_etag_path = os.environ.get("ODF_NEW_ETAG_PATH")

page = 1
while True:
    resp = requests.get(
        f"https://api.github.com/repos/{user}/{repo}/stargazers?per_page={per_page}&page={page}",
        headers={
            "X-GitHub-Api-Version": "2022-11-28",
            "Accept": "application/vnd.github.star+json",
        }
    )

    resp.raise_for_status()

    records = resp.json()

    if not records:
        break

    # Flatten {"starred_at": ..., "user": {...}}
    for record in records:
        record.update(record.pop("user"))
        print(json.dumps(record))

    page += 1
