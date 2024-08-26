import json
import os
import feedparser
import requests

user = os.environ["MEDIUM_USER"]

# TODO: This does not return all publications, only a few latest ones :(
entries = feedparser.parse(f"https://medium.com/feed/{user}")["entries"]

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