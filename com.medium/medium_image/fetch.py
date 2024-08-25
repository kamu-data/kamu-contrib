import json
import os
import feedparser
import requests

user = os.environ["MEDIUM_USER"]
#user= "kamu-data"

'''
resp = requests.get(
        f"https://medium.com/feed/{user}/",
        headers={
            "Content-Type": "application/json",
            "charset": "utf-8"
        }
    )

resp.raise_for_status()
'''

entries = feedparser.parse(f"https://medium.com/feed/{user}/")["entries"]

for entry in entries:
    # Get all entries by title and unique url id
    entry_title = entry["title"]
    entry_url = entry["id"]

    # Parse clapcount for each entry
    c = requests.get(entry_url).content.decode("utf-8")
    c = c.split("clapCount\":")[1]
    endIndex = c.index(",")
    claps = int(c[0:endIndex])

    print(json.dumps({"entry_title": entry_title, "entry_url": entry_url, "clap_count": claps}))